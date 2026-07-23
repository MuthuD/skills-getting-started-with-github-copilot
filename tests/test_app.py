import pytest

from src.app import activities


pytestmark = pytest.mark.anyio


async def test_unregister_participant_removes_email(client):
    # Arrange
    activity = activities["Chess Club"]
    email = "michael@mergington.edu"
    assert email in activity["participants"]

    # Act
    response = await client.delete(
        "/activities/Chess Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in activity["participants"]
    assert response.json()["message"] == f"Unregistered {email} for Chess Club"
