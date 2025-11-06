def test_root_response():
    from app.main import app
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == "Hello from Flask via Podman!"

