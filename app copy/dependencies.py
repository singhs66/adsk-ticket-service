from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt import decode_access_token
from sqlalchemy.orm import Session
from app.daoLayer.database import get_db
from app.daoLayer.dataModel.usersDO import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).get(payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
