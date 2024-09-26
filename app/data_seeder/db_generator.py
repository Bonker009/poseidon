from sqlalchemy.orm import Session
from app.db.session import SessionLocal 
from app.models.food import Food
from faker import Faker
import random
import os

fake = Faker()

def create_fake_food():
    return {
        "name": fake.word().capitalize() + " " + fake.word().capitalize(),
        "description": fake.text(max_nb_chars=200),
        "price": round(random.uniform(5.0, 50.0), 2),
        "cuisine_type": random.choice(["Italian", "Chinese", "Mexican", "Indian", "American"]),
        "image_url": fake.image_url(),
        "ingredients": fake.text(max_nb_chars=100),
        "preparation_time": random.randint(10, 120),
        "serving_size": random.randint(1, 10),
        "dietary_info": random.choice([None, "Vegetarian", "Vegan", "Gluten-Free", "Nut-Free"]),
        "rating": round(random.uniform(1.0, 5.0), 1),
        "is_available": random.choice([True, False]),
    }

def insert_fake_foods(db: Session, count: int = 10):
    for _ in range(count):
        fake_food = create_fake_food()
        new_food = Food(**fake_food)
        db.add(new_food)
    db.commit()

if __name__ == "__main__":
    db = SessionLocal() 
    insert_fake_foods(db, count=100) 
