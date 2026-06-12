import pytest

# Arrange-Act-Assert pattern used in each test


def test_root_redirects_to_static(client):
    # Arrange: client fixture
    # Act
    resp = client.get("/", follow_redirects=False)
    # Assert
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location") == "/static/index.html"


def test_get_activities_returns_required_fields(client):
    # Arrange
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # pick an activity and verify fields
    for name, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        break


def test_signup_success_and_then_present(client):
    # Arrange
    email = "new.student@mergington.edu"
    activity = "Chess Club"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant present
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    assert email in resp2.json()[activity]["participants"]


def test_signup_duplicate_email_rejected(client):
    # Arrange existing email
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 400


def test_signup_activity_not_found(client):
    # Arrange
    email = "someone@nowhere.edu"
    activity = "No Such Activity"
    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 404


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # Verify removed
    resp2 = client.get("/activities")
    assert email not in resp2.json()[activity]["participants"]


def test_remove_participant_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "noone@nowhere.edu"
    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 404


def test_remove_participant_activity_not_found(client):
    # Arrange
    activity = "Not An Activity"
    email = "someone@nowhere.edu"
    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 404
