from datetime import datetime
import hashlib
import os
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, get_current_user
from app.crud.user import authenticate_user
from app.db.deps import get_db
from app.schemas.user import CurrentUserResponse

router = APIRouter()


@router.get("/auth/users/me", response_model=CurrentUserResponse)
def read_current_user(
    current_user: CurrentUserResponse = Depends(get_current_user),
):
    return current_user


@router.post("/auth/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
