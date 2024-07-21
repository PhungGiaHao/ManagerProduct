# routers/category.py

from fastapi import APIRouter, Depends, HTTPException , status
from sqlalchemy.orm import Session
from app.Schema.schemas import Category, CategoryCreate  # Ensure this path is correct
from database import get_db , db_dependency
from app.Model import models
import logging

router = APIRouter()

@router.get("/", response_model=list[Category],status_code=status.HTTP_200_OK)
def read_categories(db: db_dependency, skip: int = 0, limit: int = 10):
    result = db.query(models.Category).offset(skip).limit(limit).all()
    if result is None:
        raise HTTPException(status_code=404, detail="Categories not found")
    return result

# @router.post("/", response_model=Category)
# def create_category(db: db_dependency, category: CategoryCreate):
#     existing_category = db.query(models.Category).filter_by(name=category.name).first()
#     if existing_category:
#         raise HTTPException(
#             status_code= status.HTTP_400_BAD_REQUEST,
#             detail="Category with this name already exists."
#         )
#     db_category = models.Category(name=category.name)
#     db.add(db_category)
#     db.commit()
#     db.refresh(db_category)
    
#     return db_category

@router.put("/{category_id}", response_model=Category,status_code=status.HTTP_200_OK)
def update_category(category_id: int, category_update: CategoryCreate, db: db_dependency):
    category = db.query(models.Category).filter_by(id=category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found."
        )
    existing_category = db.query(models.Category).filter_by(name=category_update.name).first()
    if existing_category and existing_category.id != category_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists."
        )
    category.name = category_update.name
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", response_model=Category,status_code=status.HTTP_200_OK)
def delete_category(category_id: int, db: db_dependency):
    category = db.query(models.Category).filter_by(id=category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found."
        )
    products_count = db.query(models.Product).filter_by(category_id=category_id).count()
    logging.info(f"Products count: {products_count}")
    if products_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category because it has associated products."
        )
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully."}