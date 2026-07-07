from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        response = client.post(f"/activities/{quote(activity_name)}/signup?email={quote(email)}")

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        response = client.delete(f"/activities/{quote(activity_name)}/participants/{quote(email)}")

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants
