import pytest
from datetime import timedelta
from fastapi import HTTPException

from app.auth.jwt import create_access_token, decode_access_token, verify_token

# Sample user payload
payload = {"sub": "user@example.com"}

def test_create_and_decode_access_token():
    token = create_access_token(payload)
    decoded = decode_access_token(token)

    assert decoded is not None
    assert decoded["sub"] == payload["sub"]

def test_expired_token_returns_none():
    # Create a token that expired 10 minutes ago
    token = create_access_token(payload, expires_delta=timedelta(minutes=-10))
    decoded = decode_access_token(token)

    assert decoded is None

def test_verify_token_success():
    token = create_access_token(payload)
    result = verify_token(token)  # simulate Depends manually
    assert result["sub"] == "user@example.com"


def test_verify_token_invalid():
    invalid_token = "invalid.jwt.token"
    with pytest.raises(HTTPException) as exc_info:
        verify_token(invalid_token)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid or expired token"

