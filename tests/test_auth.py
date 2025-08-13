def test_register_and_login_flow(client):
    r = client.post("/auth/register", json={"email": "a@a.com", "password": "abcdefg"})
    assert r.status_code == 201

    r2 = client.post("/auth/login", json={"email": "a@a.com", "password": "abcdefg"})
    assert r2.status_code == 200
    assert "access_token" in r2.get_json()
