from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def make_payload(name: str, ref: str):
    return {
        "document_text": f"Built backend systems for {name} with FastAPI and observability.",
        "reference_text": ref,
        "document_type": "resume",
        "reference_type": "job_description",
        "metadata": {"document_name": name, "reference_name": "backend_role"},
    }


def test_resume_analysis_diff_export_workflow():
    first = client.post("/v1/jobs", json=make_payload("workflow_left", "Looking for backend engineer with APIs and observability."))
    second = client.post("/v1/jobs", json=make_payload("workflow_right", "Looking for backend engineer with distributed systems and observability."))

    assert first.status_code == 200
    assert second.status_code == 200

    left_job_id = first.json()["job_id"]
    right_job_id = second.json()["job_id"]

    diff = client.post("/v1/diff", json={"left_job_id": left_job_id, "right_job_id": right_job_id})
    assert diff.status_code == 200

    export_json = client.post(f"/v1/exports/job/{left_job_id}", json={"format": "json"})
    export_md = client.post(f"/v1/exports/job/{left_job_id}", json={"format": "markdown"})

    assert export_json.status_code == 200
    assert export_md.status_code == 200


def test_batch_then_dashboard_workflow():
    batch = client.post(
        "/v1/batches",
        json={
            "jobs": [
                make_payload("batch_a", "Looking for backend engineer with APIs and observability."),
                make_payload("batch_b", "Looking for backend engineer with distributed systems and observability."),
            ]
        },
    )
    assert batch.status_code == 200
    body = batch.json()
    assert body["total_jobs"] == 2
    assert body["success_count"] == 2

    summary = client.get("/v1/dashboard/summary")
    jobs = client.get("/v1/dashboard/jobs")
    stability = client.get("/v1/dashboard/stability")

    assert summary.status_code == 200
    assert jobs.status_code == 200
    assert stability.status_code == 200
