def build_summary(jobs: dict, batches: dict) -> dict:
    total_jobs = len(jobs)
    total_batches = len(batches)

    processing_times = [
        item.get("processing_time_ms", 0)
        for item in jobs.values()
        if isinstance(item, dict)
    ]
    avg_processing_time_ms = round(sum(processing_times) / total_jobs, 2) if total_jobs else 0.0

    successful_jobs = sum(
        1 for item in jobs.values()
        if isinstance(item, dict) and item.get("status") == "completed"
    )
    success_rate = round((successful_jobs / total_jobs) * 100, 2) if total_jobs else 0.0

    return {
        "total_jobs": total_jobs,
        "total_batches": total_batches,
        "avg_processing_time_ms": avg_processing_time_ms,
        "success_rate": success_rate,
    }


def recent_jobs(jobs: dict) -> list[dict]:
    return sorted(
        jobs.values(),
        key=lambda item: item.get("created_at", ""),
        reverse=True,
    )
