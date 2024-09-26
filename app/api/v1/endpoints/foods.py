from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.food import FoodCreate, FoodResponse
from app.core.security import get_current_user, oauth2_scheme
from app.crud.food import (
    create_food,
    get_available_foods,
    get_foods,
    get_food_by_id,
    get_foods_by_cuisine,
    get_foods_by_ingredient,
    get_random_foods,
    search_foods,
    update_food,
    delete_food,
    update_food_availability,
)
from app.schemas.user import CurrentUserResponse

router = APIRouter()


@router.post("/foods/", response_model=FoodResponse)
def create_new_food(
    food: FoodCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    return create_food(db=db, food=food)


@router.get("/foods/", response_model=list[FoodResponse])
def read_foods(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    foods = get_foods(db=db, skip=skip, limit=limit)
    return foods


@router.get("/foods/ingredient/{ingredient}", response_model=list[FoodResponse])
def read_foods_by_ingredient(
    ingredient: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    foods = get_foods_by_ingredient(db=db, ingredient=ingredient)
    if not foods:
        raise HTTPException(
            status_code=404, detail="No foods found with the specified ingredient"
        )
    return foods


@router.get("/foods/cuisine/{cuisine_type}", response_model=list[FoodResponse])
def read_foods_by_cuisine(
    cuisine_type: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    foods = get_foods_by_cuisine(db=db, cuisine_type=cuisine_type)
    if not foods:
        raise HTTPException(
            status_code=404, detail="No foods found for the specified cuisine type"
        )
    return foods


@router.get("/foods/random", response_model=list[FoodResponse])
def read_random_foods(
    limit: int = 5, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    random_foods = get_random_foods(db=db, limit=limit)
    return random_foods


@router.get("/foods/search", response_model=list[FoodResponse])
def search_food(
    query: str,
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    foods = search_foods(db=db, query=query)
    if not foods:
        raise HTTPException(status_code=404, detail="No foods found")
    return foods


@router.get("/foods/available", response_model=list[FoodResponse])
def read_available_foods(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    foods = get_available_foods(db=db)
    return foods


@router.patch("/foods/{food_id}/availability", response_model=FoodResponse)
def change_food_availability(
    food_id: int,
    is_available: bool,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):

    updated_food = update_food_availability(
        db=db, food_id=food_id, is_available=is_available
    )
    return updated_food


@router.get("/foods/{food_id}", response_model=FoodResponse)
def read_food(
    food_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    food = get_food_by_id(db=db, food_id=food_id)
    if food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.put("/foods/{food_id}", response_model=FoodResponse)
def update_existing_food(
    food_id: int,
    food: FoodCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    updated_food = update_food(db=db, food_id=food_id, food_data=food)
    if updated_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return updated_food


@router.delete("/foods/{food_id}", response_model=FoodResponse)
def delete_existing_food(
    food_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    deleted_food = delete_food(db=db, food_id=food_id)
    if deleted_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return deleted_food
