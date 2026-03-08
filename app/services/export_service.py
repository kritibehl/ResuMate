import json
from uuid import uuid4

from app.schemas.export import ExportResponse


def export_job(job: dict, export_format: str) -> ExportResponse:
    if export_format == "json":
        content = json.dumps(job, indent=2)
    elif export_format == "markdown":
        analysis = job.get("analysis", {})
        matched = analysis.get("matched_requirements", [])
        gaps = analysis.get("gaps", [])
        suggestions = analysis.get("suggested_actions", [])

        lines = [
            "# ResuMate Export",
            "",
            f"- Job ID: {job['job_id']}",
            f"- Status: {job['status']}",
            f"- Schema Version: {job['schema_version']}",
            f"- Created At: {job['created_at']}",
            f"- Processing Time (ms): {job['processing_time_ms']}",
            f"- Input Fingerprint: {job['input_fingerprint']}",
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
