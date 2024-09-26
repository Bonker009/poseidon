from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class FoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    cuisine_type: str
    image_url: Optional[HttpUrl] = None   
    ingredients: Optional[str] = None  
    preparation_time: Optional[int] = None   
    serving_size: Optional[int] = None  
    dietary_info: Optional[str] = None 

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
