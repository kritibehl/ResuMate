import { fetchSummary, fetchJobs, fetchStability } from "@/lib/api";
import { DataTable, MetricCard, Nav, Page } from "@/components/ui";

export default async function HomePage() {
  const summary = await fetchSummary();
  const jobsResponse = await fetchJobs();
  const stabilityResponse = await fetchStability();

  const jobs = jobsResponse.items ?? [];
  const stability = stabilityResponse.items ?? [];

  return (
    <Page title="ResuMate Dashboard">
      <Nav />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 28 }}>
        <MetricCard label="Total Jobs" value={summary.total_jobs ?? 0} />
        <MetricCard label="Total Batches" value={summary.total_batches ?? 0} />
        <MetricCard label="Avg Processing Time" value={`${summary.avg_processing_time_ms ?? 0} ms`} />
        <MetricCard label="Success Rate" value={`${summary.success_rate ?? 0}%`} />
      </div>

      <h2 style={{ fontSize: 28, marginBottom: 12 }}>Recent Jobs</h2>
      <DataTable
        columns={["Job ID", "Status", "Created At", "Processing Time", "Fingerprint"]}
        rows={jobs.map((job: any) => [
          job.job_id,
          job.status,
          job.created_at,
          `${job.processing_time_ms} ms`,
          job.input_fingerprint,
        ])}
        emptyMessage="No jobs yet"
      />

      <div style={{ height: 28 }} />

      <h2 style={{ fontSize: 28, marginBottom: 12 }}>Stability</h2>
      <DataTable
        columns={["Fingerprint", "Repeat Count", "Job IDs"]}
        rows={stability.map((item: any) => [
          item.input_fingerprint,
          item.repeat_count,
          (item.job_ids ?? []).join(", "),
        ])}
        emptyMessage="No stability groups yet"
      />
    </Page>
  );
}
