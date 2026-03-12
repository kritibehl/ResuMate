import json
from datetime import datetime
from uuid import uuid4

from app.schemas.export import ExportResponse


def _to_json_safe(value):
    if hasattr(value, "model_dump"):
        return _to_json_safe(value.model_dump())

    if isinstance(value, dict):
        return {k: _to_json_safe(v) for k, v in value.items()}

    if isinstance(value, list):
        return [_to_json_safe(item) for item in value]

    if isinstance(value, datetime):
        return value.isoformat()

    return value


def export_job(job: dict, export_format: str) -> ExportResponse:
    safe_job = _to_json_safe(job)

    if export_format == "json":
        content = json.dumps(safe_job, indent=2)
    elif export_format == "markdown":
        analysis = safe_job.get("analysis", {})
        matched = analysis.get("matched_requirements", [])
        gaps = analysis.get("gaps", [])
        suggestions = analysis.get("suggested_actions", [])

        lines = [
            "# ResuMate Export",
            "",
            f"- Job ID: {safe_job['job_id']}",
            f"- Status: {safe_job['status']}",
            f"- Schema Version: {safe_job['schema_version']}",
            f"- Created At: {safe_job['created_at']}",
            f"- Updated At: {safe_job.get('updated_at', '')}",
            f"- Processing Time (ms): {safe_job['processing_time_ms']}",
            f"- Input Fingerprint: {safe_job['input_fingerprint']}",
            "",
            "## Analysis",
            "",
            f"- Coverage Score: {analysis.get('coverage_score', 0.0)}",
            "",
            "## Matched Requirements",
        ]

        if matched:
            for item in matched:
                lines.append(f"- {item['requirement_text']} ({item['coverage']})")
        else:
            lines.append("- None")

        lines.append("")
        lines.append("## Gaps")
        if gaps:
            for item in gaps:
                lines.append(f"- {item['requirement_text']} ({item['gap_type']})")
        else:
            lines.append("- None")

        lines.append("")
        lines.append("## Suggested Actions")
        if suggestions:
            for item in suggestions:
                lines.append(f"- {item}")
        else:
            lines.append("- None")

        content = "\n".join(lines)
    else:
        raise ValueError(f"Unsupported export format: {export_format}")

    return ExportResponse(
        export_id=f"export_{uuid4().hex[:12]}",
        format=export_format,
        content=content,
    )
