from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_db_session
from main import bcrypt_context
from schemas import LoginSchema, UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def generate_jwt_token(user_id):
    '''Function to generate a JWT token for the user'''
    token = f"ahuyba786dabd86a5vdba865dvad786and{user_id}" # Placeholder for the JWT token generation logic
    return token

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

# login -> email e senha -> token JWT (Json Web Token) ahuyba786dabd86a5vdba865dvad786and
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_db_session)):
    '''Endpoint to login a user and return a JWT token'''
    user = session.query(User).filter(User.email == login_schema.email).first()
    if not user or not bcrypt_context.verify(login_schema.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    else:
        access_token = generate_jwt_token(user.id)
        return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}