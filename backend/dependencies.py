from fastapi import Depends, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import User
from database import get_db
import os

from dotenv import load_dotenv
load_dotenv()


class Token(BaseModel):
    token: str

def get_authenticated_user(token: Token, db: Session = Depends(get_db)):
    CLIENT_ID = os.environ.get('REACT_APP_GOOGLE_CLIENT_ID')
    try:
        idinfo = id_token.verify_oauth2_token(token.token, requests.Request(), CLIENT_ID)

        if idinfo['aud'] != CLIENT_ID:
            raise ValueError('Could not verify audience.')

        user_id = idinfo['sub']

        # Check if the user exists in the database
        existing_user = db.query(User).filter(User.google_account_id == user_id).first()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        return existing_user

    except ValueError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")