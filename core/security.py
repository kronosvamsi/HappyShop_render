
# core/security.py
from datetime import datetime,timedelta
from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from db_models.models import get_db,User


SECRET_KEY = "krishna@123"
ALGORITHM = "HS256"
TOKEN_EXPIRE = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id:int):
    
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE)
    payload = {
        "sub": str(user_id),   ## user id
        "exp":expire
    }
    token =  jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

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

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = verify_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user