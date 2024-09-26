from datetime import datetime
import hashlib
import os
from typing import Annotated
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token, get_current_user
from app.db.deps import get_db
from app.models.user import User
from app.schemas.user import CurrentUserResponse, UserCreate, UserResponse, UserUpdate
from app.crud.user import (
    authenticate_user,
    create_user,
    delete_user_by_id,
    get_user_by_email,
    get_users,
    update_user_by_id,
    get_user_by_id,
)

router = APIRouter()


def hash_filename(filename: str) -> str:
    """Hashes the filename to ensure uniqueness."""
    hashed = hashlib.sha256()
    hashed.update((filename + str(datetime.utcnow())).encode("utf-8"))
    return hashed.hexdigest() + os.path.splitext(filename)[1]


@router.post("/users/", response_model=UserResponse)
async def create_new_user(
    email: str = Form(...),
    username: str = Form(...),
    full_name: str = Form(...),
    password: str = Form(...),
    profile_picture: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = UserCreate(
        email=email,
        username=username,
        full_name=full_name,
        password=password,
        profile_picture=None,
    )

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    hashed_filename = hash_filename(profile_picture.filename)
    file_location = f"uploads/{hashed_filename}"

    try:
        with open(file_location, "wb") as file:
            file.write(await profile_picture.read())

        user.profile_picture = file_location  # Set the profile picture path
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Could not save the profile picture: {str(e)}"
        )

    return create_user(db=db, user=user)


@router.get("/users/id/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    return UserResponse.from_user(user, request)


@router.get("/users", response_model=list[UserResponse])
def get_all_users(request: Request, db: Session = Depends(get_db)):
    users = get_users(db)
    return [UserResponse.from_user(user, request) for user in users]


@router.get("/users/email/{email}", response_model=UserResponse)
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)
):
    return update_user_by_id(db=db, user_id=user_id, user_update=user_update)


@router.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user_by_id(db=db, user_id=user_id)
    return deleted_user
