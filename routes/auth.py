from  fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from db_models.models import User,get_db
from data_models.pyd_models import UserModel,LoginRequest
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
def login( db: Session = Depends(get_db),form_data:OAuth2PasswordRequestForm = Depends()):

    user = auth_service.get_user_by_email(db, form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials (password)")

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }