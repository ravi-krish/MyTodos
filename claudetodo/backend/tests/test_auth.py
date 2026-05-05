from fastapi.testclient import TestClient


_EMAIL = "user@example.com"
_PASSWORD = "secret123"


def test_register(client: TestClient) -> None:
    r = client.post("/auth/register", json={"email": _EMAIL, "password": _PASSWORD})
    assert r.status_code == 200
    assert r.json() == {"message": "registered"}


def test_login(client: TestClient) -> None:
    client.post("/auth/register", json={"email": _EMAIL, "password": _PASSWORD})
    r = client.post("/auth/login", json={"email": _EMAIL, "password": _PASSWORD})
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def _get_token(client: TestClient) -> str:
    client.post("/auth/register", json={"email": _EMAIL, "password": _PASSWORD})
    r = client.post("/auth/login", json={"email": _EMAIL, "password": _PASSWORD})
    return r.json()["access_token"]


def test_todos_authenticated(client: TestClient) -> None:
    token = _get_token(client)
    r = client.get("/todos", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200


def test_todos_unauthenticated(client: TestClient) -> None:
    r = client.get("/todos")
    assert r.status_code == 401
