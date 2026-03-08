from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_endpoints_exist():
    summary = client.get("/v1/dashboard/summary")
    jobs = client.get("/v1/dashboard/jobs")
    stability = client.get("/v1/dashboard/stability")

    assert summary.status_code == 200
    assert jobs.status_code == 200
    assert stability.status_code == 200

    assert "total_jobs" in summary.json()
    assert "items" in jobs.json()
    assert "items" in stability.json()
