from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_openapi_contains_expected_paths():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    paths = data.get("paths", {})

    expected = [
        "/health",
        "/v1/jobs",
        "/v1/jobs/{job_id}",
        "/v1/history",
        "/v1/versions",
        "/v1/batches",
        "/v1/batches/{batch_id}",
        "/v1/diff",
        "/v1/exports/job/{job_id}",
        "/v1/dashboard/summary",
        "/v1/dashboard/jobs",
        "/v1/dashboard/stability",
    ]

    for path in expected:
        assert path in paths


def test_job_response_contract():
    payload = {
        "document_text": "Built FastAPI services with tracing and observability.",
        "reference_text": "Looking for backend engineer with APIs and observability.",
        "document_type": "resume",
        "reference_type": "job_description",
        "metadata": {"document_name": "contract_test", "reference_name": "backend_role"},
    }
    response = client.post("/v1/jobs", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert set(body.keys()) == {
        "job_id",
        "status",
        "schema_version",
        "created_at",
        "processing_time_ms",
        "input_fingerprint",
        "analysis",
        "errors",
    }

    assert set(body["analysis"].keys()) == {
        "coverage_score",
        "matched_requirements",
        "gaps",
        "suggested_actions",
    }
