import pytest

from src.app import activities


pytestmark = pytest.mark.anyio


async def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = await client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


async def test_get_activities_returns_expected_data(client):
    # Arrange
    path = "/activities"

    # Act
    response = await client.get(path)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert "participants" in body["Chess Club"]


async def test_signup_adds_student_when_not_already_enrolled(client):
    # Arrange
    activity_name = "Science Club"
    email = "new.student@mergington.edu"
    assert email not in activities[activity_name]["participants"]

    # Act
    response = await client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


async def test_signup_returns_400_for_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    assert existing_email in activities[activity_name]["participants"]

    # Act
    response = await client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


async def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    unknown_activity = "Robotics"
    email = "student@mergington.edu"

    # Act
    response = await client.post(
        f"/activities/{unknown_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


async def test_unregister_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    assert email in activities[activity_name]["participants"]

    # Act
    response = await client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} for {activity_name}"


async def test_unregister_returns_404_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.enrolled@mergington.edu"
    assert email not in activities[activity_name]["participants"]

    # Act
    response = await client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
