from pydantic import BaseModel, EmailStr
from pydantic.types import constr
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    password: str
    is_superuser: bool = False
