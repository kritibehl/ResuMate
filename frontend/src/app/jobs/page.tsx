"use client";

import { useEffect, useMemo, useState } from "react";
import { fetchHistory } from "@/lib/api";
import { DataTable, Nav, Page } from "@/components/ui";

type HistoryItem = {
  job_id: string;
  created_at: string;
  document_name?: string;
  reference_name?: string;
  input_fingerprint: string;
  status: string;
};

export default function JobsPage() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    fetchHistory().then((data) => setItems(data.items ?? []));
  }, []);

  const filtered = useMemo(() => {
    return items.filter((item) => {
      const matchesQuery =
        item.job_id.toLowerCase().includes(query.toLowerCase()) ||
        (item.document_name ?? "").toLowerCase().includes(query.toLowerCase()) ||
        (item.reference_name ?? "").toLowerCase().includes(query.toLowerCase());

      const matchesStatus =
        statusFilter === "all" ? true : item.status === statusFilter;

      return matchesQuery && matchesStatus;
    });
  }, [items, query, statusFilter]);

  return (
    <Page title="Job History">
      <Nav />

      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by job ID, document, or reference"
          style={{ padding: 10, minWidth: 320, border: "1px solid #d1d5db" }}
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          style={{ padding: 10, border: "1px solid #d1d5db" }}
        >
          <option value="all">All statuses</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
        </select>
      </div>

      <DataTable
        columns={["Job ID", "Status", "Document", "Reference", "Created At", "Fingerprint"]}
        rows={filtered.map((item) => [
          item.job_id,
          item.status,
          item.document_name ?? "-",
          item.reference_name ?? "-",
          item.created_at,
          item.input_fingerprint,
        ])}
        emptyMessage="No history yet"
      />
    </Page>
  );
}
