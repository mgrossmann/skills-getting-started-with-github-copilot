from fastapi import status

from src.app import activities


def test_get_activities_returns_all(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    payload = response.json()
    assert expected_activity in payload


def test_signup_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_signup(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_not_found(client):
    # Arrange
    activity_name = "Underwater Basket Weaving"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": "test@mergington.edu"})

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_success(client):
    # Arrange
    activity_name = "Chess Club"
    participant = activities[activity_name]["participants"][0]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{participant}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Removed {participant} from {activity_name}"
    assert participant not in activities[activity_name]["participants"]


def test_remove_participant_not_found(client):
    # Arrange
    activity_name = "Chess Club"
    missing_participant = "missing@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{missing_participant}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Participant not found for this activity"


def test_root_redirects_to_static(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in {status.HTTP_307_TEMPORARY_REDIRECT, status.HTTP_308_PERMANENT_REDIRECT}
    assert response.headers["location"] == expected_location
