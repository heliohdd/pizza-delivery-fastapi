from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_db_session, token_verify
from main import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, bcrypt_context
from schemas import LoginSchema, UserSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def generate_jwt_token(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    '''Function to generate a JWT token for the user'''
    data_expiration = datetime.now(timezone.utc) + token_duration  # Token expiration time in seconds (1 hour)
    dic_info = {"sub": str(user_id), "exp": data_expiration}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)  # Secret key and algorithm used for encoding
    return encoded_jwt

def authenticate_user(email: str, password: str, session: Session):
    '''Function to authenticate a user with email and password'''
    user = session.query(User).filter(User.email == email).first()
    if not user or not bcrypt_context.verify(password, user.password):
        return None
    return user

@auth_router.get("/")
async def home():
    '''Endpoint for system standard authentication'''
    return {"message": "Auth endpoint"}

@auth_router.post("/create_account")
async def create_account(user_schema: UserSchema, session: Session = Depends(get_db_session)):
    '''Endpoint to create a new user account'''
    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        password_hashed = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.username, user_schema.email, password_hashed, user_schema.active, user_schema.admin)  # Assuming User model has email and password fields
        session.add(new_user)
        session.commit()
        return {"message": f"User {user_schema.username} created successfully"}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_db_session)):
    '''Endpoint to login a user and return a JWT token'''
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user or not bcrypt_context.verify(login_schema.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    else:
        access_token = generate_jwt_token(user.id)
        refresh_token = generate_jwt_token(user.id, token_duration=timedelta(days=7))  # Refresh token valid for 7 days
        # Here you can store the refresh token in the database if needed
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "user_id": user.id}

@auth_router.get("/refresh_token")
async def use_refresh_token(user: User = Depends(token_verify)):
    access_token = generate_jwt_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }