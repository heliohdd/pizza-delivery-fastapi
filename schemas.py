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

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class OrderItemSchema(BaseModel):
    quantity: int
    flavor: str
    size: str
    unity_price: float

    class Config:
        from_attributes = True