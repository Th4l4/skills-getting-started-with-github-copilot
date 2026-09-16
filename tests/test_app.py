from fastapi.testclient import TestClient

from src.app import app
from src import app as app_module

client = TestClient(app)


def test_signup_and_unregister_participant():
    original = app_module.activities["Chess Club"]["participants"][:]
    app_module.activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.post("/activities/Chess Club/signup?email=student@mergington.edu")
    assert response.status_code == 200
    assert "student@mergington.edu" in app_module.activities["Chess Club"]["participants"]

    delete_response = client.delete("/activities/Chess Club/participants?email=student@mergington.edu")
    assert delete_response.status_code == 200
    assert "student@mergington.edu" not in app_module.activities["Chess Club"]["participants"]

    app_module.activities["Chess Club"]["participants"] = original


def test_duplicate_signup_blocked():
    original = app_module.activities["Programming Class"]["participants"][:]
    app_module.activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]

    response = client.post("/activities/Programming Class/signup?email=emma@mergington.edu")
    assert response.status_code == 400
    assert app_module.activities["Programming Class"]["participants"] == ["emma@mergington.edu", "sophia@mergington.edu"]

    app_module.activities["Programming Class"]["participants"] = original


def test_signup_checks_max_participants_and_case_insensitive_duplicates():
    original = app_module.activities["Soccer Club"]["participants"][:]
    app_module.activities["Soccer Club"]["participants"] = ["a@mergington.edu", "b@mergington.edu"]
    app_module.activities["Soccer Club"]["max_participants"] = 2

    duplicate_response = client.post("/activities/Soccer Club/signup?email=A@mergington.edu")
    assert duplicate_response.status_code == 400

    full_response = client.post("/activities/Soccer Club/signup?email=c@mergington.edu")
    assert full_response.status_code == 400
    assert app_module.activities["Soccer Club"]["participants"] == ["a@mergington.edu", "b@mergington.edu"]

    app_module.activities["Soccer Club"]["participants"] = original
    app_module.activities["Soccer Club"]["max_participants"] = 24
