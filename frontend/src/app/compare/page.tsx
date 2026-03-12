"use client";

import { useState } from "react";
import { exportJob } from "@/lib/api";
import { Nav, Page } from "@/components/ui";

export default function ComparePage() {
  const [jobId, setJobId] = useState("");
  const [format, setFormat] = useState<"json" | "markdown">("json");
  const [result, setResult] = useState<any>(null);

  async function handleExport() {
    const data = await exportJob(jobId, format);
    setResult(data);
  }

  return (
    <Page title="Run Comparison / Export">
      <Nav />

      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <input
          placeholder="Job ID"
          value={jobId}
          onChange={(e) => setJobId(e.target.value)}
          style={{ padding: 10, minWidth: 240, border: "1px solid #d1d5db" }}
        />
        <select
          value={format}
          onChange={(e) => setFormat(e.target.value as "json" | "markdown")}
          style={{ padding: 10, border: "1px solid #d1d5db" }}
        >
          <option value="json">JSON</option>
          <option value="markdown">Markdown</option>
        </select>
        <button
          onClick={handleExport}
          style={{ padding: "10px 16px", border: "1px solid #111827", background: "#111827", color: "#ffffff" }}
        >
          Export
        </button>
      </div>

      {result?.content && (
        <pre style={{ background: "#f3f4f6", padding: 16, overflow: "auto", whiteSpace: "pre-wrap", color: "#111827" }}>
          {result.content}
        </pre>
      )}

      {result?.error && (
        <div style={{ padding: 12, border: "1px solid #fecaca", background: "#fef2f2", color: "#991b1b" }}>
          {result.error}
        </div>
      )}
    </Page>
  );
}
