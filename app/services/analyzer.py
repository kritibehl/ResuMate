import re

from app.schemas.errors import ErrorItem
from app.schemas.response import AnalysisResult, GapItem, MatchedRequirement


def _extract_candidate_requirements(reference_text: str) -> list[str]:
    parts = re.split(r"[.\n;•\-]+", reference_text)
    cleaned = []
    seen = set()

    for part in parts:
        item = " ".join(part.split()).strip()
        if len(item) < 8:
            continue
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        cleaned.append(item)

    return cleaned[:8]


def _fallback_analysis(document_text: str, reference_text: str) -> AnalysisResult:
    requirements = _extract_candidate_requirements(reference_text)
    doc_lower = document_text.lower()

    matched: list[MatchedRequirement] = []
    gaps: list[GapItem] = []
    suggestions: list[str] = []

    keywords = {
        "distributed": ["distributed", "concurrency", "job processor", "locking"],
        "observability": ["prometheus", "metrics", "monitoring", "grafana", "tracing"],
        "api": ["api", "fastapi", "rest", "http"],
        "backend": ["backend", "python", "service", "microservice"],
    }

    for idx, req in enumerate(requirements, start=1):
        req_lower = req.lower()
        evidence: list[str] = []

        for family_keywords in keywords.values():
            if any(word in req_lower for word in family_keywords):
                if any(word in doc_lower for word in family_keywords):
                    evidence.append(
                        f"Document contains signals relevant to: {', '.join(family_keywords[:2])}"
                    )

        if evidence:
            matched.append(
                MatchedRequirement(
                    requirement_id=f"req_{idx}",
                    requirement_text=req,
                    coverage="partial",
                    evidence=evidence,
                    confidence=0.65,
                )
            )
        else:
            gaps.append(
                GapItem(
                    requirement_id=f"req_{idx}",
                    requirement_text=req,
                    gap_type="missing",
                    reason="No clear supporting evidence found in the document text.",
                )
            )

    if gaps:
        suggestions.append("Add stronger evidence for missing or weakly covered requirements.")
    if not matched and not gaps:
        suggestions.append("Provide a more detailed reference text to improve requirement extraction.")

    total = len(matched) + len(gaps)
    score = round(len(matched) / total, 2) if total else 0.0

    return AnalysisResult(
        coverage_score=score,
        matched_requirements=matched,
        gaps=gaps,
        suggested_actions=suggestions,
    )


def analyze_document(document_text: str, reference_text: str):
    return _fallback_analysis(document_text, reference_text), [
        ErrorItem(code="fallback_only", message="Temporary fallback-only mode enabled.")
    ]
