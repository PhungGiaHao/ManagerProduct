from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile , status
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from app.Schema.schemas import Token, User  # Ensure this path is correct
from app.utils.jwt import create_access_token, create_refresh_token
from database import db_dependency, get_db
from app.Model import models 
from passlib.hash import bcrypt
import os
from dotenv import load_dotenv
load_dotenv()
router = APIRouter()



@router.post("/register", response_model=User)
def register_user(db: db_dependency, user: User):
    existing_user = db.query(models.User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists."
        )
    #hash password
    hash = bcrypt.hash(user.password)
    db_user = models.User(username=user.username, password=hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = next(get_db())
    user = db.query(models.User).filter_by(username=form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    if not bcrypt.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)
    return {"access_token": access_token, "refresh_token": refresh_token}


