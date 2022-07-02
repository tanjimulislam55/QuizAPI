from pydantic import BaseModel, EmailStr
from pydantic.types import constr
from typing import Optional


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: constr(
        min_length=11, max_length=14, regex=r"(\+880)?[0-9]{11}"  # noqa: F722
    )
    birth_date: Optional[str]


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    birth_date: Optional[str]
    phone: Optional[
        constr(min_length=11, max_length=14, regex=r"(\+880)?[0-9]{11}")  # noqa: F722
    ]
    password: Optional[str]


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
        # arbitrary_types_allowed = True


class UserInDB(UserBase):
    password: str
    is_superuser: bool = False
