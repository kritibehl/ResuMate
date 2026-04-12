<div align="center">

# ResuMate

**Schema-validated document processing pipeline with typed contracts, multi-phase workflows, versioned artifacts, and diff/export support**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-Frontend-000000?style=flat-square&logo=nextdotjs&logoColor=white)](https://nextjs.org)

</div>

---

## What it does

ResuMate is a document transformation pipeline. Given a source document and a reference document, it:

- Validates typed request payloads against a defined Pydantic schema
- Runs a configurable multi-stage analysis workflow (phase1 → phase2 → phase3 → phase4)
- Produces structured JSON and Markdown output artifacts
- Stores analysis history for later inspection and replay
- Supports diffing across document versions for change tracking
- Exports results in machine-readable and review-friendly formats

---

## Engineering focus

Most text-analysis systems produce one-off output. ResuMate treats document transformation as a software engineering problem:

**Stable contracts** — typed request validation via Pydantic. Same input structure, every run.

**Repeatable processing** — same document produces the same artifact structure. Phase-gated, not ad hoc.

**Diffable outputs** — analysis versions can be compared. Changes are visible and reviewable, not implicit.

**Testable pipeline** — 12 FastAPI test modules covering API contract validation, schema validation, batch processing, diff view correctness, export integrity, auth audit trail, integration workflows, and output stability.

---

## System surfaces

- **FastAPI backend** — document analysis API with typed request contracts and `document_type` handling
- **Multi-phase workflow engine** — phase1 through phase4, each with structured artifacts
- **History and diff endpoints** — versioned analysis storage and cross-version comparison
- **Batch processing** — multiple documents in a single request
- **Next.js frontend** — document submission and review UI
- **Streamlit dashboard** — analysis history, diff view, and export controls

---

## Example output

```json
{
  "document_type": "technical",
  "phase": "phase3",
  "artifact_id": "a1b2c3d4",
  "version": "2025-03-01T14:22:11Z",
  "analysis": {
    "sections_identified": 4,
    "structured_output": { }
  }
}
```

---

## Test coverage

12 FastAPI test modules:

- API contract validation (valid and invalid inputs)
- Schema validation
- Batch processing behavior
- Diff view correctness across versions
- Export format integrity (JSON and Markdown)
- Auth audit trail
- Integration workflows across phases
- Output stability — same input produces same artifact structure

---

## Running

```bash
# Backend
uvicorn main:app --reload

# Tests
pytest tests/ -v

# Dashboard
streamlit run dashboard/app.py
```

---

## Stack

Python · FastAPI · Pydantic · Next.js · Streamlit · SQLite · Docker

---

## Interview framing

ResuMate is a document transformation pipeline. The engineering focus is on making text processing repeatable and verifiable: typed schemas, phase-gated workflows, diffable outputs, and test coverage that validates output structure rather than just API response codes. The use case is a vehicle for demonstrating contract-first API design and reproducible pipeline architecture.

---

## Related

- [AutoOps-Insight](https://github.com/kritibehl/AutoOps-Insight) — CI failure intelligence pipeline
- [FairEval](https://github.com/kritibehl/FairEval-Suite) — structured evaluation pipeline for AI systems
- [AgentGrid-Demo](https://github.com/kritibehl/agentgrid-demo) — agentic document triage workflow
