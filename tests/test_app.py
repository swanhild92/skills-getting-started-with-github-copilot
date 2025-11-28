import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity keys
    assert "Chess Club" in data

def test_signup_and_unregister_cycle():
    activity = "Chess Club"
    email = "pytest.user@example.com"

    # Ensure clean state: remove if already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for {activity}"
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400

    # Unregister
    resp3 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp3.status_code == 200
    assert resp3.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 404
    resp4 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp4.status_code == 404
