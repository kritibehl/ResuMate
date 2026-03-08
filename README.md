# ResuMate

**An API-first workflow engine for structured document analysis and repeatable automation.**

ResuMate accepts single and batch document-analysis jobs, returns schema-validated JSON outputs, tracks history and input versions, supports diffing between runs, exports results in JSON and Markdown, and exposes summary and stability metrics through a lightweight dashboard.

---

## What It Does

ResuMate solves a structured workflow problem: given a source document (for example, a resume) and a reference document (for example, a job description), it processes them as a backend job and returns stable, machine-readable output that can be inspected, compared, and exported.

This is not an AI resume writer. The core problem is **repeatable document-analysis workflow with stable contracts**, and that is what the system is designed around.

---

## Key Features

- **Structured job API** — Submit document pairs as jobs with a stable JSON response contract
- **Input fingerprinting** — SHA-256 of normalized input for repeatability and deduplication
- **Batch processing** — Submit multiple jobs in one request and retrieve aggregate results
- **Version tracking** — Each job creates a version record for traceability during the current runtime session
- **History** — List recent jobs with metadata
- **Diff view** — Compare two job runs and see what changed between them
- **Exports** — Download results as JSON or Markdown
- **Dashboard** — Summary metrics, recent jobs, and stability grouping via a Streamlit UI

---
## Current Prototype Snapshot

- **12 API endpoints**
- **7 workflow capabilities**: jobs, history, versions, batches, diff, exports, dashboard
- **2 export formats**: JSON, Markdown
- **34 Python source files**
- **10 test files**
- **5 passing smoke tests**

## API Overview

### Core

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/v1/jobs` | Submit a new analysis job |
| `GET` | `/v1/jobs/{job_id}` | Retrieve a job by ID |
| `GET` | `/v1/history` | List recent jobs |
| `GET` | `/v1/versions` | List version records |

### Batch

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/batches` | Submit multiple jobs at once |
| `GET` | `/v1/batches/{batch_id}` | Retrieve batch summary |

### Diff & Export

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/diff` | Compare two job runs |
| `POST` | `/v1/exports/job/{job_id}` | Export a job (JSON or Markdown) |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/v1/dashboard/summary` | Aggregate counts and metrics |
| `GET` | `/v1/dashboard/jobs` | Recent job list |
| `GET` | `/v1/dashboard/stability` | Stability grouping by fingerprint |

---

## Response Schema

Every job response returns a stable, schema-versioned payload:

```json
{
  "job_id": "job_123abc",
  "status": "completed",
  "schema_version": "1.0.0",
  "created_at": "2026-03-08T06:35:27.008820Z",
  "processing_time_ms": 1,
  "input_fingerprint": "sha256:...",
  "analysis": {
    "coverage_score": 1.0,
    "matched_requirements": [
      {
        "requirement_id": "req_1",
        "requirement_text": "Looking for backend engineer with APIs and observability",
        "coverage": "partial",
        "evidence": [
          "Document contains signals relevant to: api, fastapi"
        ],
        "confidence": 0.65
      }
    ],
    "gaps": [],
    "suggested_actions": []
  },
  "errors": []
}
```

Diff responses include:

```json
{
  "left_job_id": "...",
  "right_job_id": "...",
  "coverage_score_change": +0.12,
  "added_requirements": ["..."],
  "removed_requirements": [],
  "changed_suggestions": ["..."]
}
```

---

## Project Structure

```
app/
├── api/          # Route layer (jobs, batches, versions, exports, dashboard)
├── schemas/      # Request/response models, domain models, error models
├── services/     # Business logic (analysis, batching, diffing, exports, metrics)
├── storage/      # Persistence layer (in-memory; designed for Mongo restoration)
└── utils/        # Shared helpers (hashing, timing)
dashboard/        # Streamlit dashboard
prompts/          # Prompt templates
tests/            # Smoke tests for phases 1–4
```

---

## Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API
uvicorn app.main:app --reload --port 8002

# Start the dashboard (separate terminal)
streamlit run dashboard/streamlit_app.py
```

---

## Running Tests

```bash
python3 -m pytest -q tests/test_phase1_smoke.py tests/test_phase2_smoke.py tests/test_phase3_smoke.py tests/test_phase4_smoke.py
```

Tests cover the job lifecycle, batch submission, diff, and export flows.

---

## Architecture Notes

### Analyzer

The current analyzer uses a rule-based fallback mode that produces schema-valid output using heuristic matching. This keeps the API contract stable and the system fully testable while the model-backed analysis path is in development.

### Storage

State is currently held in-memory for local prototyping. The storage layer is structured to support Mongo-backed persistence, but persistence is temporarily disabled while the local/managed connection path is being restored. In the current prototype, state does not survive restarts.

### Fingerprinting

Inputs are normalized and hashed with SHA-256 before processing. This enables:
- Deduplication detection
- Stability grouping (repeated inputs surfaced in the dashboard)
- Reasoning about output consistency across runs

---

## What's Next

1. **Restore Mongo persistence** — replace in-memory storage with a local or managed cluster
2. **Re-enable model-backed analysis** — controlled integration with structured output validation
3. **Expand test coverage** — contract tests, regression tests, stability suites
4. **Dashboard improvements** — richer visualizations, filtering, and export from UI

---

## Design Philosophy

ResuMate is framed as an **internal tooling system**, not a consumer AI product. The emphasis is on:

- Stable API contracts over free-form generation
- Repeatable, traceable workflow execution
- Structured outputs that are testable, exportable, and automatable
- Operational visibility through metrics and dashboarding

The "resume analysis" use case is the vehicle. The backend system is the point.