def test_task_crud(client, auth_headers):
    # create
    r = client.post("/tasks/", json={"title": "First", "description": "d1"}, headers=auth_headers)
    assert r.status_code == 201
    tid = r.get_json()["id"]

    # get
    r = client.get(f"/tasks/{tid}", headers=auth_headers)
    assert r.status_code == 200
    assert r.get_json()["title"] == "First"

    # update
    r = client.put(f"/tasks/{tid}", json={"completed": True}, headers=auth_headers)
    assert r.status_code == 200
    assert r.get_json()["completed"] is True

    # list
    r = client.get("/tasks/?page=1&per_page=5&completed=true", headers=auth_headers)
    assert r.status_code == 200
    data = r.get_json()
    assert data["total"] >= 1
    assert data["items"][0]["completed"] is True

    # delete
    r = client.delete(f"/tasks/{tid}", headers=auth_headers)
    assert r.status_code in (204, 200)
