const BASE_URL = "http://127.0.0.1:8002/v1";

async function safeFetch(path: string, options?: RequestInit) {
  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      cache: "no-store",
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {}),
      },
    });

    if (!res.ok) {
      return { error: `Request failed: ${res.status}` };
    }

    return await res.json();
  } catch (error) {
    return { error: "Backend unavailable. Start FastAPI on port 8002." };
  }
}

export async function fetchSummary() {
  return safeFetch("/dashboard/summary");
}

export async function fetchJobs() {
  return safeFetch("/dashboard/jobs");
}

export async function fetchStability() {
  return safeFetch("/dashboard/stability");
}

export async function fetchHistory() {
  return safeFetch("/history");
}

export async function createJob(payload: any) {
  return safeFetch("/jobs", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function exportJob(jobId: string, format: "json" | "markdown") {
  return safeFetch(`/exports/job/${jobId}`, {
    method: "POST",
    body: JSON.stringify({ format }),
  });
}

export async function postDiff(left_job_id: string, right_job_id: string) {
  return safeFetch("/diff", {
    method: "POST",
    body: JSON.stringify({ left_job_id, right_job_id }),
  });
}
