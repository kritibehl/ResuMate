from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def make_payload(name: str):
    return {
        "document_text": f"Built a distributed job processor for {name} with Prometheus metrics.",
        "reference_text": "Looking for backend engineer with distributed systems and observability.",
        "document_type": "resume",
        "reference_type": "job_description",
        "metadata": {
            "document_name": name,
            "reference_name": "backend_role",
        },
    }


def test_history_versions_and_batch():
    r1 = client.post("/v1/jobs", json=make_payload("resume_v1"))
    assert r1.status_code == 200

    history = client.get("/v1/history")
    assert history.status_code == 200
    assert "items" in history.json()
    assert len(history.json()["items"]) >= 1

    versions = client.get("/v1/versions")
    assert versions.status_code == 200
    assert "items" in versions.json()
    assert len(versions.json()["items"]) >= 1

    batch = client.post(
        "/v1/batches",
        json={"jobs": [make_payload("resume_v2"), make_payload("resume_v3")]},
    )
    assert batch.status_code == 200
    body = batch.json()
    assert body["batch_id"].startswith("batch_")
    assert body["total_jobs"] == 2
    assert body["success_count"] == 2
    assert len(body["job_ids"]) == 2

    batch_get = client.get(f"/v1/batches/{body['batch_id']}")
    assert batch_get.status_code == 200
    assert batch_get.json()["batch_id"] == body["batch_id"]
