# schemas.py

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, validator
from enum import Enum

class CategoryBase(BaseModel):
    name: str = 'Category Name'

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock_level: int
    imageurl: str
    inventory: int
    category_id: int = 1

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductInventory(BaseModel):
    id: int
    name: str
    inventory: int
    category: str

    class Config:
        from_attributes = True

# class CategoryEnum(str, Enum):
#     electronics = "Electronics"
#     clothing = "clothing"
#     home_appliances = "home_appliances"
#     books = "books"



class OrderCreate(BaseModel):
    product_id: int
    quantity: int
    weight: float = Field(..., gt=0, description="Weight of the parcel in kg")

class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    weight: float
    shipping_cost: float
    total_cost: float

class FileUploadResponse(BaseModel):
    file_url: str


class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str