from fastapi import Depends,APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime

from database import get_db
from models import User

from sqlalchemy.orm import Session

router = APIRouter()

class UserResponse(BaseModel):
    id: int
    google_account_id: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    google_account_id: str
    email: EmailStr

# POST /users: Create a new user
@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db = SessionLocal()

    # Check if the user already exists
    existing_user = db.query(User).filter(User.google_account_id == user.google_account_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Check if email is already taken
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email is already taken")

    # Create a new user
    new_user = User(google_account_id=user.google_account_id, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user