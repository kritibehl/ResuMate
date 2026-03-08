def build_stability_report(jobs: dict) -> list[dict]:
    grouped: dict[str, list[dict]] = {}

    for item in jobs.values():
        fingerprint = item.get("input_fingerprint", "unknown")
        grouped.setdefault(fingerprint, []).append(item)

    report = []
    for fingerprint, records in grouped.items():
        report.append(
            {
                "input_fingerprint": fingerprint,
                "repeat_count": len(records),
                "job_ids": [record.get("job_id") for record in records],
            }
        )

    return sorted(report, key=lambda item: item["repeat_count"], reverse=True)
