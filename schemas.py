from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    active: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    user_id: int 

    class Config:
        from_attributes = True