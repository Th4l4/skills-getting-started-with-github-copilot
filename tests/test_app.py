from fastapi.testclient import TestClient

from src.app import app
from src import app as app_module

client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    original_participants = app_module.activities[activity_name]["participants"][:]

    # Arrange
    app_module.activities[activity_name]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    # Act: sign the participant up
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: signup succeeded and participant is present
    assert response.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]

    # Act: unregister the participant
    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert: participant is removed
    assert delete_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]

    app_module.activities[activity_name]["participants"] = original_participants


def test_duplicate_signup_blocked():
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    original_participants = app_module.activities[activity_name]["participants"][:]

    # Arrange
    app_module.activities[activity_name]["participants"] = [
        "emma@mergington.edu",
        "sophia@mergington.edu",
    ]

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert app_module.activities[activity_name]["participants"] == [
        "emma@mergington.edu",
        "sophia@mergington.edu",
    ]

    app_module.activities[activity_name]["participants"] = original_participants


def test_signup_checks_max_participants_and_case_insensitive_duplicates():
    activity_name = "Soccer Club"
    original_participants = app_module.activities[activity_name]["participants"][:]
    original_max = app_module.activities[activity_name]["max_participants"]

    # Arrange
    app_module.activities[activity_name]["participants"] = [
        "a@mergington.edu",
        "b@mergington.edu",
    ]
    app_module.activities[activity_name]["max_participants"] = 2

    # Act
    duplicate_response = client.post(f"/activities/{activity_name}/signup?email=A@mergington.edu")
    full_response = client.post(f"/activities/{activity_name}/signup?email=c@mergington.edu")

    # Assert
    assert duplicate_response.status_code == 400
    assert full_response.status_code == 400
    assert app_module.activities[activity_name]["participants"] == [
        "a@mergington.edu",
        "b@mergington.edu",
    ]

    app_module.activities[activity_name]["participants"] = original_participants
    app_module.activities[activity_name]["max_participants"] = original_max
