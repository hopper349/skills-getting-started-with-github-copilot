"""
Tests for the High School Management System API
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    baseline = deepcopy(activities)
    yield
    activities.clear()
    activities.update(deepcopy(baseline))


def test_get_activities(client):
    # Arrange
    expected_keys = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Art Studio", "Drama Club", "Math Club", "Robotics Club"
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for key in expected_keys:
        assert key in data


def test_signup_for_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    before = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == before + 1


def test_signup_duplicate_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_missing_activity_404(client):
    # Arrange
    activity_name = "Invalid Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    before = len(activities[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == before - 1


def test_remove_missing_participant_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "noone@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_remove_missing_activity_404(client):
    # Arrange
    activity_name = "Invalid Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
