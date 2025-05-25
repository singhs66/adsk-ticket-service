from sqlalchemy.orm import Session
from app.daoLayer.dataModel.usersDO import User
from app.auth.security import verify_password


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password):
        return user
    return None
