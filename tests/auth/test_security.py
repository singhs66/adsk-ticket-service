from app.auth.security import hash_password, verify_password


def test_hash_and_verify_password_success():
    raw_password = "securePass123!"
    hashed = hash_password(raw_password)

    assert hashed != raw_password  # Ensure it's actually hashed
    assert verify_password(raw_password, hashed) is True


def test_verify_password_failure():
    hashed = hash_password("correct_password")

    assert verify_password("wrong_password", hashed) is False
