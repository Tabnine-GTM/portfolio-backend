def test_login_success(client):
    response = client.post(
        "/auth/login", json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Logged in successfully"}
    assert "portfolio_auth" in response.cookies
    assert "refresh_token" in response.cookies


def test_login_failure(client):
    response = client.post(
        "/auth/login", json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_refresh_token(client):
    # First, login to get a refresh token
    login_response = client.post(
        "/auth/login", json={"username": "testuser", "password": "testpassword"}
    )
    assert login_response.status_code == 200

    # Now use the refresh token to get a new access token
    refresh_response = client.post("/auth/refresh")
    assert refresh_response.status_code == 200
    assert refresh_response.json() == {"message": "Token refreshed successfully"}
    assert "portfolio_auth" in refresh_response.cookies
    assert "refresh_token" in refresh_response.cookies


def test_logout(client):
    response = client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}
    assert "portfolio_auth" not in response.cookies
    assert "refresh_token" not in response.cookies


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "password": "newpassword",
            "email": "new@example.com",
        },
    )
    assert response.status_code == 200
    assert "message" in response.json()
    assert "user" in response.json()
    assert "portfolio_auth" in response.cookies
    assert "refresh_token" in response.cookies
