from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email():
    activity = activities["Chess Club"]
    original_participants = list(activity["participants"])

    try:
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"},
        )

        assert response.status_code == 200
        assert "michael@mergington.edu" not in activity["participants"]
        assert response.json()["message"] == "Unregistered michael@mergington.edu for Chess Club"
    finally:
        activity["participants"] = original_participants
