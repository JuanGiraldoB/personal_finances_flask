def test_request_example(client):
    response = client.get("/dashboard")
    assert response.status_code == 200