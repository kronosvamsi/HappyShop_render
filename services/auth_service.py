from fastapi import HTTPException,status
from db_models.models import User


def get_user_by_email(session, email):
    user_email = session.query(User).filter(User.email == email).first()
    return user_email

    pass

def create_user(session,firstname,email,hash_password):
    user = User(firstname= firstname,email=email,hashed_password=hash_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    pass