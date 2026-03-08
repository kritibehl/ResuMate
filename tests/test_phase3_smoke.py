from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def make_payload(name: str, ref: str):
    return {
        "document_text": f"Built FastAPI services with Prometheus and tracing for {name}.",
        "reference_text": ref,
        "document_type": "resume",
        "reference_type": "job_description",
        "metadata": {
            "document_name": name,
            "reference_name": "backend_role",
        },
    }


def test_diff_and_export():
    left = client.post(
        "/v1/jobs",
        json=make_payload("resume_diff_left", "Looking for backend engineer with APIs and observability."),
    )
    right = client.post(
        "/v1/jobs",
        json=make_payload("resume_diff_right", "Looking for backend engineer with distributed systems and observability."),
    )

    assert left.status_code == 200
    assert right.status_code == 200

    left_job_id = left.json()["job_id"]
    right_job_id = right.json()["job_id"]

    diff = client.post(
        "/v1/diff",
        json={"left_job_id": left_job_id, "right_job_id": right_job_id},
    )
    assert diff.status_code == 200
    diff_body = diff.json()
    assert diff_body["left_job_id"] == left_job_id
    assert diff_body["right_job_id"] == right_job_id
    assert "coverage_score_change" in diff_body
    assert "added_requirements" in diff_body
    assert "removed_requirements" in diff_body
    assert "changed_suggestions" in diff_body

    export_json = client.post(f"/v1/exports/job/{left_job_id}", json={"format": "json"})
    assert export_json.status_code == 200
    assert export_json.json()["format"] == "json"

    export_md = client.post(f"/v1/exports/job/{left_job_id}", json={"format": "markdown"})
    assert export_md.status_code == 200
    assert export_md.json()["format"] == "markdown"
