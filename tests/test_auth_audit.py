from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def make_payload(name: str = "auth_case"):
    return {
        "document_text": "Built FastAPI services with tracing and observability.",
        "reference_text": "Looking for backend engineer with APIs and observability.",
        "document_type": "resume",
        "reference_type": "job_description",
        "metadata": {
            "document_name": name,
            "reference_name": "backend_role",
        },
    }


def test_create_job_forbidden_for_viewer():
    response = client.post(
        "/v1/jobs",
        json=make_payload(),
        headers={"x-user-id": "viewer1", "x-user-role": "viewer"},
    )
    assert response.status_code == 403


def test_create_job_allowed_for_editor():
    response = client.post(
        "/v1/jobs",
        json=make_payload("editor_case"),
        headers={"x-user-id": "editor1", "x-user-role": "editor"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["job_id"].startswith("job_")


def test_audit_requires_admin():
    response = client.get(
        "/v1/audit",
        headers={"x-user-id": "editor1", "x-user-role": "editor"},
    )
    assert response.status_code == 403


def test_audit_lists_job_create_and_export_events():
    create = client.post(
        "/v1/jobs",
        json=make_payload("audit_case"),
        headers={"x-user-id": "admin1", "x-user-role": "admin"},
    )
    assert create.status_code == 200
    job_id = create.json()["job_id"]

    export = client.post(
        f"/v1/exports/job/{job_id}",
        json={"format": "json"},
        headers={"x-user-id": "admin1", "x-user-role": "admin"},
    )
    assert export.status_code == 200

    audit = client.get(
        "/v1/audit",
        headers={"x-user-id": "admin1", "x-user-role": "admin"},
    )
    assert audit.status_code == 200

    items = audit.json()["items"]
    assert len(items) >= 2
    actions = [item["action"] for item in items]
    assert "job.create" in actions
    assert "job.export" in actions
