from app.schemas.export import DiffResponse


def compare_jobs(left_job: dict, right_job: dict) -> DiffResponse:
    left_requirements = {
        item["requirement_text"]
        for item in left_job.get("analysis", {}).get("matched_requirements", [])
    }
    right_requirements = {
        item["requirement_text"]
        for item in right_job.get("analysis", {}).get("matched_requirements", [])
    }

    left_suggestions = set(left_job.get("analysis", {}).get("suggested_actions", []))
    right_suggestions = set(right_job.get("analysis", {}).get("suggested_actions", []))

    left_score = float(left_job.get("analysis", {}).get("coverage_score", 0.0))
    right_score = float(right_job.get("analysis", {}).get("coverage_score", 0.0))

    return DiffResponse(
        left_job_id=left_job["job_id"],
        right_job_id=right_job["job_id"],
        coverage_score_change=round(right_score - left_score, 2),
        added_requirements=sorted(list(right_requirements - left_requirements)),
        removed_requirements=sorted(list(left_requirements - right_requirements)),
        changed_suggestions=sorted(list(left_suggestions ^ right_suggestions)),
    )
