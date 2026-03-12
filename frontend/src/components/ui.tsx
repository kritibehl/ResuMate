import React from "react";

export function Page({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <main style={{ minHeight: "100vh", background: "#ffffff", color: "#111827", padding: 24, fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ fontSize: 44, marginBottom: 20 }}>{title}</h1>
      {children}
    </main>
  );
}

export function Nav() {
  return (
    <div style={{ marginBottom: 24, fontSize: 18 }}>
      <a href="/" style={{ color: "#111827", textDecoration: "none" }}>Dashboard</a>
      <span> | </span>
      <a href="/jobs" style={{ color: "#111827", textDecoration: "none" }}>Job History</a>
      <span> | </span>
      <a href="/diff" style={{ color: "#111827", textDecoration: "none" }}>Diff Visualization</a>
      <span> | </span>
      <a href="/compare" style={{ color: "#111827", textDecoration: "none" }}>Run Comparison</a>
    </div>
  );
}

export function MetricCard({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div style={{ border: "1px solid #d1d5db", padding: 18, background: "#ffffff" }}>
      <div style={{ fontSize: 20, fontWeight: 700, marginBottom: 10 }}>{label}</div>
      <div style={{ fontSize: 24 }}>{value}</div>
    </div>
  );
}

export function DataTable({
  columns,
  rows,
  emptyMessage = "No data",
}: {
  columns: string[];
  rows: React.ReactNode[][];
  emptyMessage?: string;
}) {
  const cell: React.CSSProperties = {
    border: "1px solid #d1d5db",
    padding: "10px 12px",
    textAlign: "left",
    verticalAlign: "top",
    color: "#111827",
    backgroundColor: "#ffffff",
    fontSize: 14,
  };

  const headerCell: React.CSSProperties = {
    ...cell,
    fontWeight: 700,
    backgroundColor: "#f3f4f6",
  };

  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", backgroundColor: "#ffffff" }}>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column} style={headerCell}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td style={cell} colSpan={columns.length}>{emptyMessage}</td>
            </tr>
          ) : (
            rows.map((row, i) => (
              <tr key={i}>
                {row.map((value, j) => (
                  <td key={j} style={cell}>{value}</td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
