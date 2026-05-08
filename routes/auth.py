from  fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from db_models.models import User
from db_models.db import get_db
from data_models.pyd_models import UserModel,LoginRequest,RefreshToken
from services import auth_service
from core.security import hash_password,verify_password,create_access_token

router = APIRouter(
    prefix= "/auth",
    tags=["auth"],
    dependencies=[Depends(get_db)]
)
### User Registration
@router.post("/register")
def register(user:UserModel, session:Session = Depends(get_db)):
    user_exist = auth_service.get_user_by_email(session,user.email)
    # print("User: ",user)
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    new_user = auth_service.create_user(session,user.firstname,user.email,hashed_password)
    # print("db user:", new_user)
    return JSONResponse(content={"message":"Registered successfully"})


@router.post("/login")
def login(form_data:LoginRequest, db: Session = Depends(get_db)):

    # print("form", form_data)

    user = auth_service.get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials (password)")
    
    token = auth_service.login_user(db,user)
    return token

@router.post("/refresh")
def refresh(token: RefreshToken, db: Session = Depends(get_db)):

    # print("Refresh token", refresh_token)

    return auth_service.refresh_access_token(db, token.refresh_token)

@router.post("/logout")
def refresh(token: RefreshToken, db: Session = Depends(get_db)):

    return auth_service.logout_user(db, token.refresh_token)

