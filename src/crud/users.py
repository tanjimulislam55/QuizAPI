from typing import Optional
from sqlalchemy import select

from schemas.users import UserCreate, UserUpdate
from models import User
from .base import CRUDBase
from utils.db import database


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_one_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        return await database.fetch_one(query)

    async def get_one_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        return await database.fetch_one(query)


user = CRUDUser(User)
