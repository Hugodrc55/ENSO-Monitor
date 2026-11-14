"""Contrat HTTP de la route de santé, qui ne dépend pas de la base de données.

La route filtrée des observations est testée dans test_observations_api.py.
"""

from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_service_status() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok", "service": "enso-monitor-api"}
