from fastapi import APIRouter, Depends
from models import User
from dependencies import get_db_session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    '''Endpoint for system standard authentication'''
    return {"message": "Auth endpoint"}

@auth_router.post("/create_account")
async def create_account(username: str, email: str, password: str, session= Depends(get_db_session)):
    '''Endpoint to create a new user account'''
    user = session.query(User).filter(User.email == email).first()
    if user:
        return {"message": "User already exists"}
    else:
        new_user = User(username, email, password)  # Assuming User model has email and password fields
        # new_user = User(username=username, email=email, password=password)  # Assuming User model has email and password fields
        session.add(new_user)
        session.commit()
        return {"message": "User created successfully"}
