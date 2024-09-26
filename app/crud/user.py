from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password
from sqlalchemy.exc import SQLAlchemyError


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def get_user_by_email(db: Session, email: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"No user found with email: {email}"
        )
    return user


def get_user_by_id(db: Session, user_id: int):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(db: Session, user: UserCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    try:
        hashed_password = hash_password(user.password)
        new_user = User(
            email=user.email,
            hashed_password=hashed_password,
            profile_picture=user.profile_picture,
            full_name=user.full_name,
            username=user.username,
            is_active=True,
            created_at=func.now(),
            updated_at=func.now(),
            role=UserRole.user,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database transaction failed: {str(e)}"
        )


def get_users(db: Session):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


def update_user_by_id(db: Session, user_id: int, user_update: UserUpdate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.full_name:
        user.full_name = user_update.full_name
    if user_update.profile_picture:
        user.profile_picture = user_update.profile_picture
    if user_update.username:
        user.username = user_update.username
    if user_update.password:
        user.hashed_password = hash_password(user_update.password)
    user.updated_at = func.now()

    try:
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database transaction failed: {str(e)}"
        )


def delete_user_by_id(db: Session, user_id: int):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        deleted_user = user
        db.delete(user)
        db.commit()
        return deleted_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database transaction failed: {str(e)}"
        )
