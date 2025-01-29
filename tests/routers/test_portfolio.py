def test_get_portfolio_unauthorized(client):
    response = client.get("/portfolio")
    assert response.status_code == 401


# Add more tests here that use authenticated requests
