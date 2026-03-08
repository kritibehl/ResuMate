from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job():
    payload = {
        "document_text": "Built a distributed job processor with lease-based locking, retries, Prometheus metrics, and failure recovery.",
        "reference_text": "Looking for backend engineer with distributed systems, observability, and API experience.",
        "document_type": "resume",
        "reference_type": "job_description",
        "metadata": {
            "document_name": "resume_v1",
            "reference_name": "backend_role",
        },
    }

    response = client.post("/v1/jobs", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["job_id"].startswith("job_")
    assert body["status"] == "completed"
    assert body["schema_version"] == "1.0.0"
    assert body["processing_time_ms"] >= 1
    assert body["input_fingerprint"].startswith("sha256:")
    assert "analysis" in body
    assert "matched_requirements" in body["analysis"]
    assert "gaps" in body["analysis"]
    assert "suggested_actions" in body["analysis"]
    assert "errors" in body
