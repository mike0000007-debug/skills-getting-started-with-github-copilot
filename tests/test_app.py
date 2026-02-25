from src import app as app_module
from src.app import activities


def test_get_activities(client):
    # Arrange: client fixture is provided
    # Act
    r = client.get("/activities")
    # Assert
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    assert email not in activities[activity]["participants"]
    # Act
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert r.status_code == 200
    assert r.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in activities[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    existing = activities[activity]["participants"][0]
    # Act
    r = client.post(f"/activities/{activity}/signup", params={"email": existing})
    # Assert
    assert r.status_code == 400
    assert r.json()["detail"] == "Student already signed up for this activity"


def test_signup_missing_activity(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "x@mergington.edu"
    # Act
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert r.status_code == 404
    assert r.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    assert email in activities[activity]["participants"]
    # Act
    r = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert r.status_code == 200
    assert r.json() == {"message": f"Unregistered {email} from {activity}"}
    assert email not in activities[activity]["participants"]


def test_unregister_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "notattending@mergington.edu"
    assert email not in activities[activity]["participants"]
    # Act
    r = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert r.status_code == 404
    assert r.json()["detail"] == "Student not found in this activity"


def test_unregister_missing_activity(client):
    # Arrange
    activity = "No Such Activity"
    email = "x@mergington.edu"
    # Act
    r = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert r.status_code == 404
    assert r.json()["detail"] == "Activity not found"


def test_root_redirect(client):
    # Arrange/Act
    r = client.get("/", follow_redirects=False)
    # Assert
    assert r.status_code in (302, 307)
    assert r.headers.get("location") == "/static/index.html"
