from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_invalid_job_payload_missing_fields():
    response = client.post("/v1/jobs", json={})
    assert response.status_code == 422


def test_invalid_batch_payload_shape():
    response = client.post("/v1/batches", json={"jobs": [{}]})
    assert response.status_code == 422
