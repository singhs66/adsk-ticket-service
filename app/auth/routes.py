from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.apiSchemas import UserCreate
from app.daoLayer.database import get_db
from app.auth.authenticate import authenticate_user
from app.auth.jwt import create_access_token
from app.daoLayer.dataModel.usersDO import User
from app.auth.security import hash_password

router = APIRouter()


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        active=True
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created"}
