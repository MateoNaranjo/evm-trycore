import pytest

from tests.integration.conftest import OVERSPENT_ACTIVITY


def test_create_activity_returns_201_with_calculated_metrics(client, project_id):
    response = client.post(f"/api/projects/{project_id}/activities", json=OVERSPENT_ACTIVITY)

    assert response.status_code == 201
    body = response.json()
    assert body["project_id"] == project_id
    assert body["name"] == "Diseño"
    assert body["budget_at_completion"] == 10000
    assert body["metrics"] == {
        "budget_at_completion": 10000.0,
        "planned_value": 5000.0,
        "earned_value": 4000.0,
        "actual_cost": 6000.0,
        "cost_variance": -2000.0,
        "schedule_variance": -1000.0,
        "cost_performance_index": 0.6667,
        "schedule_performance_index": 0.8,
        "estimate_at_completion": 15000.0,
        "variance_at_completion": -5000.0,
        "cost_status": "OVER_BUDGET",
        "schedule_status": "BEHIND_SCHEDULE",
    }


def test_create_activity_with_zero_actual_cost_returns_null_cost_indices(client, project_id):
    payload = {**OVERSPENT_ACTIVITY, "actual_cost": 0}

    response = client.post(f"/api/projects/{project_id}/activities", json=payload)

    metrics = response.json()["metrics"]
    assert response.status_code == 201
    assert metrics["cost_performance_index"] is None
    assert metrics["estimate_at_completion"] is None
    assert metrics["cost_status"] == "NOT_AVAILABLE"


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("name", ""),
        ("budget_at_completion", 0),
        ("planned_percentage", 101),
        ("actual_percentage", -1),
        ("actual_cost", -5),
        ("budget_at_completion", 10.555),
    ],
)
def test_create_activity_with_invalid_data_returns_422(
    client, project_id, field_name, invalid_value
):
    payload = {**OVERSPENT_ACTIVITY, field_name: invalid_value}

    response = client.post(f"/api/projects/{project_id}/activities", json=payload)

    assert response.status_code == 422


def test_create_activity_in_missing_project_returns_404(client):
    response = client.post("/api/projects/999/activities", json=OVERSPENT_ACTIVITY)

    assert response.status_code == 404
    assert response.json() == {"detail": "Proyecto 999 no existe."}


def test_update_activity_recalculates_metrics(client, project_id):
    activity = client.post(
        f"/api/projects/{project_id}/activities", json=OVERSPENT_ACTIVITY
    ).json()
    payload = {**OVERSPENT_ACTIVITY, "actual_percentage": 60}

    response = client.put(
        f"/api/projects/{project_id}/activities/{activity['id']}", json=payload
    )

    assert response.status_code == 200
    assert response.json()["metrics"]["earned_value"] == 6000.0
    assert response.json()["metrics"]["cost_status"] == "ON_BUDGET"
    assert response.json()["metrics"]["schedule_status"] == "AHEAD_OF_SCHEDULE"


def test_update_missing_activity_returns_404(client, project_id):
    response = client.put(
        f"/api/projects/{project_id}/activities/999", json=OVERSPENT_ACTIVITY
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Actividad 999 no existe en el proyecto {project_id}."
    }


def test_delete_activity_removes_it_from_project(client, project_id):
    activity = client.post(
        f"/api/projects/{project_id}/activities", json=OVERSPENT_ACTIVITY
    ).json()

    response = client.delete(f"/api/projects/{project_id}/activities/{activity['id']}")

    assert response.status_code == 204
    assert client.get(f"/api/projects/{project_id}").json()["activities"] == []


def test_delete_missing_activity_returns_404(client, project_id):
    response = client.delete(f"/api/projects/{project_id}/activities/999")

    assert response.status_code == 404
