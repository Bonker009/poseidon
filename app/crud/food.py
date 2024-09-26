import random
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.data_seeder.db_generator import create_fake_food
from app.models.food import Food
from app.schemas.food import FoodCreate




def get_food_by_id(db: Session, food_id: int):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


def get_foods(db: Session, skip: int = 0, limit: int = 10):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    foods = db.query(Food).offset(skip).limit(limit).all()
    if not foods:
        raise HTTPException(status_code=404, detail="No foods found")
    return foods


def create_food(db: Session, food: FoodCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    try:
        new_food = Food(
            name=food.name,
            description=food.description,
            price=food.price,
            cuisine_type=food.cuisine_type,
            image_url=food.image_url,
            ingredients=food.ingredients,
            preparation_time=food.preparation_time,
            serving_size=food.serving_size,
            dietary_info=food.dietary_info,
            rating=food.rating,
            is_available=food.is_available,
        )
        db.add(new_food)
        db.commit()
        db.refresh(new_food)
        return new_food
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database transaction failed: {str(e)}"
        )


def update_food(db: Session, food_id: int, food_data: FoodCreate):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    food = get_food_by_id(db, food_id)
    if food:
        for key, value in food_data.dict(exclude_unset=True).items():
            setattr(food, key, value)
        food.updated_at = func.now()
        try:
            db.commit()
            db.refresh(food)
            return food
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database transaction failed: {str(e)}"
            )
    return None


def delete_food(db: Session, food_id: int):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    food = get_food_by_id(db, food_id)
    if food:
        try:
            db.delete(food)
            db.commit()
            return food
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database transaction failed: {str(e)}"
            )
    return None


def get_foods_by_ingredient(db: Session, ingredient: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    foods = db.query(Food).filter(Food.ingredients.ilike(f"%{ingredient}%")).all()
    return foods


def get_foods_by_cuisine(db: Session, cuisine_type: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    foods = db.query(Food).filter(Food.cuisine_type == cuisine_type).all()
    return foods


def get_random_foods(db: Session, limit: int = 5):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    foods = db.query(Food).all()
    if not foods:
        raise HTTPException(status_code=404, detail="No foods found")
    return random.sample(foods, min(limit, len(foods)))


def search_foods(db: Session, query: str):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    foods = (
        db.query(Food)
        .filter(Food.name.ilike(f"%{query}%") | Food.description.ilike(f"%{query}%"))
        .all()
    )
    return foods


def get_available_foods(db: Session):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    foods = db.query(Food).filter(Food.is_available == True).all()
    if not foods:
        raise HTTPException(status_code=404, detail="No foods avaiable")
    return foods


def update_food_availability(db: Session, food_id: int, is_available: bool):
    if db is None:
        raise HTTPException(status_code=500, detail="Database session is not available")
    food = get_food_by_id(db, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    food.is_available = is_available
    try:
        db.commit()
        db.refresh(food)
        return food
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Database transaction failed: {str(e)}"
        )
