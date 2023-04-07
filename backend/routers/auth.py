from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
from models import User
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.environ.get('REACT_APP_GOOGLE_CLIENT_ID')

class Token(BaseModel):
    token: str

@router.post("/authenticate")
async def authenticate(token: Token, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(token.token, requests.Request(), CLIENT_ID)

        if idinfo['aud'] != CLIENT_ID:
            raise ValueError('Could not verify audience.')

        user_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        picture = idinfo['picture']

        # Check if the user already exists in the database
        existing_user = db.query(User).filter(User.google_account_id == user_id).first()

        # If the user does not exist, create a new user
        if not existing_user:
            new_user = User(google_account_id=user_id, email=email)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            existing_user = new_user

        # Return the user's information
        return {
            "google_account_id": existing_user.google_account_id,
            "email": existing_user.email,
            "name": name,
            "picture": picture,
            "created_at": existing_user.created_at,
            "updated_at": existing_user.updated_at
        }

    except ValueError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")
