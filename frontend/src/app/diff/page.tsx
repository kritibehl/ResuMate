"use client";

import { useState } from "react";
import { postDiff } from "@/lib/api";
import { DataTable, Nav, Page } from "@/components/ui";

export default function DiffPage() {
  const [leftJobId, setLeftJobId] = useState("");
  const [rightJobId, setRightJobId] = useState("");
  const [result, setResult] = useState<any>(null);

  async function handleCompare() {
    const data = await postDiff(leftJobId, rightJobId);
    setResult(data);
  }

  return (
    <Page title="Diff Visualization">
      <Nav />

      <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
        <input
          placeholder="Left Job ID"
          value={leftJobId}
          onChange={(e) => setLeftJobId(e.target.value)}
          style={{ padding: 10, minWidth: 220, border: "1px solid #d1d5db" }}
        />
        <input
          placeholder="Right Job ID"
          value={rightJobId}
          onChange={(e) => setRightJobId(e.target.value)}
          style={{ padding: 10, minWidth: 220, border: "1px solid #d1d5db" }}
        />
        <button
          onClick={handleCompare}
          style={{ padding: "10px 16px", border: "1px solid #111827", background: "#111827", color: "#ffffff" }}
        >
          Compare
        </button>
      </div>

      {result && !result.error && (
        <>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 24 }}>
            <div style={{ border: "1px solid #d1d5db", padding: 16 }}>
              <strong>Left Job</strong>
              <div>{result.left_job_id}</div>
            </div>
            <div style={{ border: "1px solid #d1d5db", padding: 16 }}>
              <strong>Right Job</strong>
              <div>{result.right_job_id}</div>
            </div>
            <div style={{ border: "1px solid #d1d5db", padding: 16 }}>
              <strong>Coverage Score Change</strong>
              <div>{result.coverage_score_change}</div>
            </div>
          </div>

          <DataTable
            columns={["Added Requirements", "Removed Requirements", "Changed Suggestions"]}
            rows={[
              [
                (result.added_requirements ?? []).join(", ") || "-",
                (result.removed_requirements ?? []).join(", ") || "-",
                (result.changed_suggestions ?? []).join(", ") || "-",
              ],
            ]}
          />
        </>
      )}

      {result?.error && (
        <div style={{ padding: 12, border: "1px solid #fecaca", background: "#fef2f2", color: "#991b1b" }}>
          {result.error}
        </div>
      )}
    </Page>
  );
}
