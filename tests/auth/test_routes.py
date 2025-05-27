import pytest
from fastapi.testclient import TestClient
from main import app  # or app.app_init if split
from app.auth.jwt import decode_access_token

client = TestClient(app)

# Shared test user credentials
test_user = {
    "name": "Test User",
    "email": "testuser@example.com",
    "password": "MySecurePass123"
}

def test_register_user_success():
    res = client.post("/register", json=test_user)
    assert res.status_code in [200, 409]  # allow already registered case

def test_register_user_conflict():
    res = client.post("/register", json=test_user)
    assert res.status_code == 409 or "already exists" in res.text

def test_login_success():
    data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    res = client.post("/token", data=data)
    assert res.status_code == 200
    token = res.json()["access_token"]
    decoded = decode_access_token(token)
    assert "sub" in decoded

def test_login_wrong_password():
    res = client.post("/token", data={
        "username": test_user["email"],
        "password": "wrongpassword"
    })
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid credentials"

