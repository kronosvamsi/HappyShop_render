from fastapi import HTTPException,status
from db_models.models import User
from jose import jwt
from core.security import SECRET_KEY, ALGORITHM
from core.security import hash_token,create_access_token,create_refresh_token
from db_models.models import UserSession
from datetime import datetime,timedelta

def get_user_by_email(session, email):
    user_email = session.query(User).filter(User.email == email).first()
    return user_email

def create_user(session,firstname,email,hash_password):
    user = User(firstname= firstname,email=email,hashed_password=hash_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    

def login_user(db, user):

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    session = UserSession(
        user_id=user.id,
        refresh_token_hash=hash_token(refresh_token),
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    db.add(session)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "username":user.firstname,
        "user_id":user.id
    }

def refresh_access_token(db, refresh_token):

    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    token_hash = hash_token(refresh_token)
    session = db.query(UserSession).filter(
        UserSession.refresh_token_hash == token_hash,
        
    ).first()

    if not session:
        raise Exception("Invalid refresh token")
    if session.revoked:
        db.query(UserSession).filter(
            UserSession.user_id == session.user_id
        ).update({"revoked":True})
        
        db.commit()
        raise HTTPException(401, detail="Refresh access token reuse detected, all sessions revoked ")

    # revoke old refresh token
    session.revoked = True

    # create new tokens
    new_access = create_access_token(user_id)

    new_refresh = create_refresh_token(user_id)
    
    new_session = UserSession(
        user_id=user_id,
        refresh_token_hash=hash_token(new_refresh),
        expires_at=datetime.utcnow() + timedelta(days=7)
    )

    db.add(new_session)
    db.commit()

    return {
        "access_token": new_access,
        "refresh_token": new_refresh
    }

def logout_user(db, refresh_token):

    token_hash = hash_token(refresh_token)

    session = db.query(UserSession).filter(
        UserSession.refresh_token_hash == token_hash
    ).first()

    if session:
        session.revoked = True
        db.commit()

    return {"message": "Logged out"}