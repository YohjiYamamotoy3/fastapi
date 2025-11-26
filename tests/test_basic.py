from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data

def test_register():
    resp = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()

def test_register_duplicate():
    client.post("/auth/register", json={
        "username": "duplicate",
        "email": "dup@example.com",
        "password": "pass123"
    })
    resp = client.post("/auth/register", json={
        "username": "duplicate",
        "email": "dup@example.com",
        "password": "pass123"
    })
    assert resp.status_code == 400

def test_login():
    client.post("/auth/register", json={
        "username": "logintest",
        "email": "login@example.com",
        "password": "password123"
    })
    resp = client.post("/auth/login", json={
        "username": "logintest",
        "password": "password123"
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()

def test_login_wrong_password():
    client.post(
        "/auth/register",
        json={
            "username": "wrongpass",
            "email": "wrong@example.com",
            "password": "correct123"
        }
    )
    response = client.post(
        "/auth/login",
        json={
            "username": "wrongpass",
            "password": "wrongpass123"
        }
    )
    assert response.status_code == 401

def test_create_task():
    reg_resp = client.post("/auth/register", json={
        "username": "taskuser",
        "email": "task@example.com",
        "password": "taskpass123"
    })
    token = reg_resp.json()["access_token"]
    
    resp = client.post("/tasks", json={
        "title": "Test Task",
        "description": "This is a test task"
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 201
    assert resp.json()["title"] == "Test Task"

def test_get_tasks():
    reg = client.post("/auth/register", json={
        "username": "gettasks",
        "email": "get@example.com",
        "password": "pass123"
    })
    token = reg.json()["access_token"]
    
    client.post("/tasks", json={
        "title": "Task 1",
        "description": "Description 1"
    }, headers={"Authorization": f"Bearer {token}"})
    
    resp = client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert len(resp.json()) > 0

