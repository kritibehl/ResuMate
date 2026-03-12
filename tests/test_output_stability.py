from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def payload():
    return {
        "document_text": "Built FastAPI services with tracing and observability.",
        "reference_text": "Looking for backend engineer with APIs and observability.",
        "document_type": "resume",
        "reference_type": "job_description",
        "metadata": {"document_name": "stability_case", "reference_name": "backend_role"},
    }


def test_repeated_input_keeps_same_fingerprint():
    first = client.post("/v1/jobs", json=payload())
    second = client.post("/v1/jobs", json=payload())

    assert first.status_code == 200
    assert second.status_code == 200

    assert first.json()["input_fingerprint"] == second.json()["input_fingerprint"]
