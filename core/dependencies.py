# from fastapi.security import OAuth2PasswordBearer
# from fastapi import Depends, HTTPException, status
# from db_models.models import get_db
# from jose import jwt

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     email = payload.get("sub")

#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user
