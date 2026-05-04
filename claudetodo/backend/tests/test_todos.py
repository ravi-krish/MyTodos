from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_get_todos_empty(client: TestClient) -> None:
    r = client.get("/todos")
    assert r.status_code == 200
    assert r.json() == []


def test_create_todo(client: TestClient) -> None:
    r = client.post("/todos", json={"title": "Buy milk"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Buy milk"
    assert body["completed"] is False
    assert body["id"] is not None
    assert "created_at" in body


def test_get_todos_returns_created(client: TestClient) -> None:
    client.post("/todos", json={"title": "Task A"})
    r = client.get("/todos")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_filter_pending(client: TestClient) -> None:
    client.post("/todos", json={"title": "Pending"})
    todo_id = client.post("/todos", json={"title": "Done"}).json()["id"]
    client.put(f"/todos/{todo_id}", json={"completed": True})
    r = client.get("/todos?status=pending")
    titles = [t["title"] for t in r.json()]
    assert titles == ["Pending"]


def test_filter_completed(client: TestClient) -> None:
    todo_id = client.post("/todos", json={"title": "Done"}).json()["id"]
    client.put(f"/todos/{todo_id}", json={"completed": True})
    r = client.get("/todos?status=completed")
    assert len(r.json()) == 1
    assert r.json()[0]["completed"] is True


def test_update_todo_title(client: TestClient) -> None:
    todo_id = client.post("/todos", json={"title": "Old"}).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={"title": "New"})
    assert r.status_code == 200
    assert r.json()["title"] == "New"


def test_update_todo_completed(client: TestClient) -> None:
    todo_id = client.post("/todos", json={"title": "Task"}).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert r.status_code == 200
    assert r.json()["completed"] is True


def test_update_todo_not_found(client: TestClient) -> None:
    r = client.put("/todos/9999", json={"completed": True})
    assert r.status_code == 404


def test_delete_todo(client: TestClient) -> None:
    todo_id = client.post("/todos", json={"title": "Delete me"}).json()["id"]
    r = client.delete(f"/todos/{todo_id}")
    assert r.status_code == 204
    assert client.get("/todos").json() == []


def test_delete_todo_not_found(client: TestClient) -> None:
    r = client.delete("/todos/9999")
    assert r.status_code == 404
