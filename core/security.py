
# core/security.py
from datetime import datetime,timedelta
from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer,HTTPBearer,HTTPAuthorizationCredentials
from db_models.models import User
from db_models.db import get_db
import hashlib
import uuid

SECRET_KEY = "krishna@123"
ALGORITHM = "HS256"
TOKEN_EXPIRE = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(user_id:int):
    
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE)
    payload = {
        "sub": str(user_id),   ## user id
        "exp":expire
    }
    token =  jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_refresh_token(user_id: int):

    payload = {
        "user_id": user_id,
        "jti": str(uuid.uuid4()),
        "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("payload",payload)
        user_id: int = int(payload.get("sub"))

        if user_id is None:
            raise HTTPException(status_code=401, detail="UnAuthorized user")

        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or token Expired")

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):  
    token = credentials.credentials
    user_id = verify_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

