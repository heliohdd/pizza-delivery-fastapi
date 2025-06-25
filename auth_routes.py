from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_db_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

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
