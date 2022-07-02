from typing import List, Optional
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from schemas.users import UserOut, UserCreate, UserInDB, UserUpdate
from schemas.token import Token
from models import User
from ...dependencies import get_current_active_superuser, get_current_user
from crud.users import user
from settings import settings
from utils.auth import create_access_token, verify_password, get_password_hash

router = APIRouter()


@router.get("/", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def get_multiple_users(
    current_user: User = Depends(get_current_active_superuser),
    skip: int = 0,
    limit: int = 10,
):
    return await user.get_many(skip, limit)


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_a_user(
    user_id: int, current_user: User = Depends(get_current_active_superuser)
):
    return await user.get_one(user_id)


@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user_me(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    if not await user.get_one(user_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await user.update(user_id, user_update)
    return {**user_update.dict(exclude_unset=True), "id": user_id}


@router.delete("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def remove_user_me(
    user_id: int, current_user: User = Depends(get_current_active_superuser)
):
    if not await user.get_one(user_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await user.remove(user_id)
    return {"message": "deleted successfully"}


@router.post("/sign_up", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_in: UserCreate):
    user_info = await user.get_one_by_email(user_in.email)
    if user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already taken",
        )
    user_info = await user.get_one_by_username(user_in.username)
    if user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken",
        )
    user_dict = user_in.dict(exclude={"password"})
    password = get_password_hash(user_in.password)
    user_dict.update({"password": password, "is_superuser": False})
    new_generated_id = await user.create(UserInDB(**user_dict))
    return {**user_in.dict(), "id": new_generated_id}


@router.post("/sign_in", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_info = await user.get_one_by_username(form_data.username)
    if not user_info or not verify_password(form_data.password, user_info.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user_info.username, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
