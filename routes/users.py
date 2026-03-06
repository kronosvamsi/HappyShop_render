from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from db_models.models import User,get_db
from data_models.pyd_models import UserModel
from fastapi.security import OAuth2PasswordRequestForm
from core.dependencies import get_current_user
from core.security import hash_password,verify_password,create_access_token

router = APIRouter(
    prefix = "/users",
    tags=["users"],
    dependencies = [Depends(get_db)]
)

@router.get("/")
async def get_users(session:Session = Depends(get_db)):
    try:
        db_users = session.query(User).all()
        if len(db_users) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The users list in db is empty")
        
       
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    except Exception as e:
        session.rollback()
        print(f"Log- unhandled exception {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Unexpected error came in process "

        )
    data_items = [UserModel.model_validate(userobj).model_dump() for userobj in db_users]
    return JSONResponse(content={"message":"Usermodel items fetched from DB","items":data_items},status_code=200)


@router.get("/user/{user_id}")
def get_user_by_id(user_id:int, session:Session = Depends(get_db)):
    try:
        db_user = session.get(User, user_id)
        if db_user is None:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The user id - {user_id} not found")
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    data_item = UserModel.model_validate(db_user).model_dump()
    return JSONResponse(content= {"message":"The userobj by id fetched ","item":data_item},status_code=200)

@router.post('/addUser')
def addUser(new_user:UserModel, session:Session = Depends(get_db)):
    try:
        user_obj=new_user.model_dump()
        if len(user_obj.keys()) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "The user obj is empty")
        
        db_user_obj=User(**user_obj)
        session.add(db_user_obj)
        session.commit()
        session.refresh(db_user_obj)
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    
    return JSONResponse(content= "User with ID added",status_code=200)


@router.put("updateUser/{user_id}")
def update_user(user_id:int, update_user:UserModel, session:Session = Depends(get_db)):
    try:
        db_user=session.get(User,user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details= f"The user id - {user_id} not found")
        
        update_user_obj=update_user.model_dump()
        for key,val in update_user_obj.items():
            setattr(db_user,key,val)
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    
    return JSONResponse(content=f"The user ID-{user_id} is updated",status_code=200)

@router.delete('/deleteUser/{user_id}')
def delete_user(user_id:int, session:Session = Depends(get_db)):
    try:
        db_user = session.get(User, user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The User with ID - {user_id} not found")
        
        session.delete(db_user)
        session.commit()

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    

    return JSONResponse(content= f"The user ID {user_id} deleted ",status_code=200)


@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    hashed_pw = hash_password(password)
    user = User(email=email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}


# @router.post("/login")
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     user = db.query(User).filter(User.email == form_data.username).first()

#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials"
#         )

#     token = create_access_token({"sub": user.email, "role": user.role})
#     return {"access_token": token, "token_type": "bearer"}


# @router.get("/profile")
# def get_profile(current_user: User = Depends(get_current_user)):
#     return {
#         "email": current_user.email,
#         "role": current_user.role
#     }


# def require_role(role: str):
#     def role_checker(user: User = Depends(get_current_user)):
#         if user.role != role:
#             raise HTTPException(status_code=403, detail="Access denied")
#         return user
#     return role_checker
