from fastapi.testclient import TestClient


def test_health(authed_client: TestClient) -> None:
    r = authed_client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_get_todos_empty(authed_client: TestClient) -> None:
    r = authed_client.get("/todos")
    assert r.status_code == 200
    assert r.json() == []


def test_create_todo(authed_client: TestClient) -> None:
    r = authed_client.post("/todos", json={"title": "Buy milk"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Buy milk"
    assert body["completed"] is False
    assert body["id"] is not None
    assert "created_at" in body


def test_get_todos_returns_created(authed_client: TestClient) -> None:
    authed_client.post("/todos", json={"title": "Task A"})
    r = authed_client.get("/todos")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_filter_pending(authed_client: TestClient) -> None:
    authed_client.post("/todos", json={"title": "Pending"})
    todo_id = authed_client.post("/todos", json={"title": "Done"}).json()["id"]
    authed_client.put(f"/todos/{todo_id}", json={"completed": True})
    r = authed_client.get("/todos?status=pending")
    titles = [t["title"] for t in r.json()]
    assert titles == ["Pending"]


def test_filter_completed(authed_client: TestClient) -> None:
    todo_id = authed_client.post("/todos", json={"title": "Done"}).json()["id"]
    authed_client.put(f"/todos/{todo_id}", json={"completed": True})
    r = authed_client.get("/todos?status=completed")
    assert len(r.json()) == 1
    assert r.json()[0]["completed"] is True


def test_update_todo_title(authed_client: TestClient) -> None:
    todo_id = authed_client.post("/todos", json={"title": "Old"}).json()["id"]
    r = authed_client.put(f"/todos/{todo_id}", json={"title": "New"})
    assert r.status_code == 200
    assert r.json()["title"] == "New"


def test_update_todo_completed(authed_client: TestClient) -> None:
    todo_id = authed_client.post("/todos", json={"title": "Task"}).json()["id"]
    r = authed_client.put(f"/todos/{todo_id}", json={"completed": True})
    assert r.status_code == 200
    assert r.json()["completed"] is True


def test_update_todo_not_found(authed_client: TestClient) -> None:
    r = authed_client.put("/todos/9999", json={"completed": True})
    assert r.status_code == 404


def test_delete_todo(authed_client: TestClient) -> None:
    todo_id = authed_client.post("/todos", json={"title": "Delete me"}).json()["id"]
    r = authed_client.delete(f"/todos/{todo_id}")
    assert r.status_code == 204
    assert authed_client.get("/todos").json() == []


def test_delete_todo_not_found(authed_client: TestClient) -> None:
    r = authed_client.delete("/todos/9999")
    assert r.status_code == 404
