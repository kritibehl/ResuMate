from app.schemas.export import DiffResponse


def _as_dict(value):
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return value or {}


def compare_jobs(left_job: dict, right_job: dict) -> DiffResponse:
    left_analysis = _as_dict(left_job.get("analysis"))
    right_analysis = _as_dict(right_job.get("analysis"))

    left_requirements = {
        item["requirement_text"]
        for item in left_analysis.get("matched_requirements", [])
    }
    right_requirements = {
        item["requirement_text"]
        for item in right_analysis.get("matched_requirements", [])
    }

    left_suggestions = set(left_analysis.get("suggested_actions", []))
    right_suggestions = set(right_analysis.get("suggested_actions", []))

    left_score = float(left_analysis.get("coverage_score", 0.0))
    right_score = float(right_analysis.get("coverage_score", 0.0))

    return DiffResponse(
        left_job_id=left_job["job_id"],
        right_job_id=right_job["job_id"],
        coverage_score_change=round(right_score - left_score, 2),
        added_requirements=sorted(right_requirements - left_requirements),
        removed_requirements=sorted(left_requirements - right_requirements),
        changed_suggestions=sorted(left_suggestions ^ right_suggestions),
    )
