from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.session import Base



class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    cuisine_type = Column(String(length=50), nullable=False)
    image_url = Column(String, nullable=True)
    ingredients = Column(Text, nullable=True)
    preparation_time = Column(Integer, nullable=True)
    serving_size = Column(Integer, nullable=True)
    dietary_info = Column(String(length=100), nullable=True)
    rating = Column(Float, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Food(name={self.name}, price={self.price}, cuisine_type={self.cuisine_type})>"
