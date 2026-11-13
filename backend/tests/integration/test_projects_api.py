from tests.integration.conftest import EFFICIENT_ACTIVITY, OVERSPENT_ACTIVITY

METRIC_FIELDS = {
    "budget_at_completion",
    "planned_value",
    "earned_value",
    "actual_cost",
    "cost_variance",
    "schedule_variance",
    "cost_performance_index",
    "schedule_performance_index",
    "estimate_at_completion",
    "variance_at_completion",
    "cost_status",
    "schedule_status",
}


def test_create_project_returns_201_with_empty_metrics(client):
    response = client.post(
        "/api/projects", json={"name": "  Portal de clientes  ", "description": "Fase 1"}
    )

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"id", "name", "description", "activities", "metrics"}
    assert body["name"] == "Portal de clientes"
    assert body["activities"] == []
    assert set(body["metrics"]) == METRIC_FIELDS
    assert body["metrics"]["budget_at_completion"] == 0
    assert body["metrics"]["cost_performance_index"] is None
    assert body["metrics"]["cost_status"] == "NOT_AVAILABLE"


def test_create_project_with_blank_name_returns_422(client):
    response = client.post("/api/projects", json={"name": "   "})

    assert response.status_code == 422


def test_list_projects_returns_summaries_with_consolidated_metrics(client, project_id):
    client.post(f"/api/projects/{project_id}/activities", json=OVERSPENT_ACTIVITY)

    response = client.get("/api/projects")

    assert response.status_code == 200
    [summary] = response.json()
    assert set(summary) == {"id", "name", "description", "activity_count", "metrics"}
    assert summary["activity_count"] == 1
    assert summary["metrics"]["earned_value"] == 4000


def test_get_project_returns_activities_and_budget_weighted_metrics(client, project_id):
    client.post(f"/api/projects/{project_id}/activities", json=OVERSPENT_ACTIVITY)
    client.post(f"/api/projects/{project_id}/activities", json=EFFICIENT_ACTIVITY)

    response = client.get(f"/api/projects/{project_id}")

    assert response.status_code == 200
    body = response.json()
    assert [activity["name"] for activity in body["activities"]] == ["Diseño", "Desarrollo"]
    assert body["metrics"]["budget_at_completion"] == 30000
    assert body["metrics"]["cost_performance_index"] == 1.0
    assert body["metrics"]["schedule_performance_index"] == 1.0
    assert body["metrics"]["cost_status"] == "ON_BUDGET"


def test_get_missing_project_returns_404_with_detail(client):
    response = client.get("/api/projects/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Proyecto 999 no existe."}


def test_update_project_replaces_name_and_description(client, project_id):
    response = client.put(
        f"/api/projects/{project_id}", json={"name": "Portal v2", "description": None}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Portal v2"
    assert response.json()["description"] is None


def test_update_missing_project_returns_404(client):
    response = client.put("/api/projects/999", json={"name": "No existe"})

    assert response.status_code == 404


def test_delete_project_removes_it_and_its_activities(client, project_id):
    activity = client.post(
        f"/api/projects/{project_id}/activities", json=OVERSPENT_ACTIVITY
    ).json()

    response = client.delete(f"/api/projects/{project_id}")

    assert response.status_code == 204
    assert client.get(f"/api/projects/{project_id}").status_code == 404
    orphan_update = client.put(
        f"/api/projects/{project_id}/activities/{activity['id']}", json=OVERSPENT_ACTIVITY
    )
    assert orphan_update.status_code == 404


def test_delete_missing_project_returns_404(client):
    response = client.delete("/api/projects/999")

    assert response.status_code == 404
