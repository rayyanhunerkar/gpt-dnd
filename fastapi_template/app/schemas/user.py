from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

__all__ = (
    'UserBase',
    'Register',
    'Login',
    'User',
    'UserResponse'
)


class UserBase(BaseModel):
    email: EmailStr = Field(...)


class Register(UserBase):
    name: str = Field(...)
    password: str = Field(...)
    confirm_password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "foobar@gmail.com",
                "name": "Foobar",
                "password": "foobar@12345",
                "confirm_password": "foobar@12345"
            }
        }


class Login(UserBase):
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "foobar@gmail.com",
                "password": "foobar@12345"
            }
        }


class User(UserBase):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    data: User
    message: str
