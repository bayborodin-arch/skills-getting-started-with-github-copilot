from urllib.parse import quote


def test_get_activities(client):
    # Arrange: none
    # Act
    r = client.get("/activities")

    # Assert
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success_and_duplicate(client):
    # Arrange
    activity = "Chess Club"
    path = quote(activity, safe="")
    email = "t1@example.com"

    # Act: sign up
    r1 = client.post(f"/activities/{path}/signup", params={"email": email})

    # Assert
    assert r1.status_code == 200

    # Act: duplicate signup
    r2 = client.post(f"/activities/{path}/signup", params={"email": email})
    assert r2.status_code == 400


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    path = quote("NoSuchActivity", safe="")

    # Act
    r = client.post(f"/activities/{path}/signup", params={"email": "a@b.com"})

    # Assert
    assert r.status_code == 404


def test_unregister_success_and_not_signed(client):
    # Arrange
    activity = "Soccer Team"
    path = quote(activity, safe="")
    email = "remove_me@example.com"

    # Ensure signup succeeds
    rs = client.post(f"/activities/{path}/signup", params={"email": email})
    assert rs.status_code == 200

    # Act: remove
    rd = client.delete(f"/activities/{path}/signup", params={"email": email})
    assert rd.status_code == 200

    # Act: remove again (should be 400)
    rd2 = client.delete(f"/activities/{path}/signup", params={"email": email})
    assert rd2.status_code == 400
