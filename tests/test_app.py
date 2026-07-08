import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client


def test_unregister_participant_removes_email(client):
    activity_name = "Temp Activity"
    email = "student@example.com"
    app_module.activities[activity_name] = {
        "description": "Temporary test activity",
        "schedule": "Mondays",
        "max_participants": 5,
        "participants": [email],
    }

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]

    app_module.activities.pop(activity_name, None)


def test_unregister_missing_participant_returns_not_found(client):
    activity_name = "Temp Activity"
    app_module.activities[activity_name] = {
        "description": "Temporary test activity",
        "schedule": "Mondays",
        "max_participants": 5,
        "participants": [],
    }

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": "missing@example.com"},
    )

    assert response.status_code == 404
    app_module.activities.pop(activity_name, None)
