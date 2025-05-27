from sqlalchemy.orm import Session
from app.auth.authenticate import authenticate_user
from app.auth.security import hash_password
from app.daoLayer.dataModel.usersDO import User
from app.daoLayer.database import SessionLocal  # or your test session

# Setup a test user
def create_test_user(db: Session, email="test@example.com", password="password123"):
    user = User(
        name="Test User",
        email=email,
        password=hash_password(password),  # hashed password
        active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_authenticate_user_success():
    db = SessionLocal()
    create_test_user(db, "user1@example.com", "secret123")

    user = authenticate_user(db, "user1@example.com", "secret123")
    assert user is not None
    assert user.email == "user1@example.com"

def test_authenticate_user_wrong_password():
    db = SessionLocal()
    create_test_user(db, "user2@example.com", "secret123")

    user = authenticate_user(db, "user2@example.com", "wrongpass")
    assert user is None

def test_authenticate_user_no_user():
    db = SessionLocal()
    user = authenticate_user(db, "missing@example.com", "whatever")
    assert user is None


