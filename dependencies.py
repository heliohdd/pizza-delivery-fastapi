from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import User, db
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt

def get_db_session():
    '''Dependency to get a database session'''
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def token_verify(token: str = Depends(oauth2_schema), session: Session = Depends(get_db_session)):
    '''Function to verify the JWT token'''
    try:
        # Decode the token to get user information
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dic_info.get("sub"))
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Access token is invalid or expired")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user