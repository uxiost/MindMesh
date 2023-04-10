from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from models import LLMIdentity, User
from database import get_db

import secrets

from dependencies import get_authenticated_user, Token

router = APIRouter()

class LLMIdentityCreate(BaseModel):
    user_id: int
    model_name: str
    model_id: str

class LLMIdentityOut(LLMIdentityCreate):
    id: int
    api_token: str

    class Config:
        orm_mode = True

class LLMIdentityUpdate(BaseModel):
    model_name: str
    api_token: str

class LLMIdentityListOut(LLMIdentityOut):
    pass

# POST /llm-identities: Create a new LLM identity
@router.post("/llm-identities", response_model=LLMIdentityOut)
def create_llm_identity(llm_identity: LLMIdentityCreate, db: Session = Depends(get_db)):
    # Check if the user exists
    user = db.query(User).filter(User.id == llm_identity.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    api_token = secrets.token_hex(32)  # Generate a random 64-character API token

    # Create a new LLM identity
    new_llm_identity = LLMIdentity(
        user_id=llm_identity.user_id,
        model_name=llm_identity.model_name,
        model_id=llm_identity.model_id,
        api_token=api_token,
    )
    db.add(new_llm_identity)
    db.commit()
    db.refresh(new_llm_identity)

    return new_llm_identity

# GET /llm-identities/:id: Retrieve LLM identity details
@router.get("/llm-identities/{id}", response_model=LLMIdentityOut)
def get_llm_identity(id: int, db: Session = Depends(get_db)):
    llm_identity = db.query(LLMIdentity).filter(LLMIdentity.id == id).first()
    if not llm_identity:
        raise HTTPException(status_code=404, detail="LLM Identity not found")

    return llm_identity

# PUT /llm-identities/:id: Update LLM identity details
@router.put("/llm-identities/{id}", response_model=LLMIdentityOut)
def update_llm_identity(id: int, llm_identity_update: LLMIdentityUpdate, db: Session = Depends(get_db)):
    llm_identity = db.query(LLMIdentity).filter(LLMIdentity.id == id).first()
    if not llm_identity:
        raise HTTPException(status_code=404, detail="LLM Identity not found")

    llm_identity.model_name = llm_identity_update.model_name
    llm_identity.api_token = llm_identity_update.api_token
    db.commit()
    db.refresh(llm_identity)

    return llm_identity

# DELETE /llm-identities/:id: Delete an LLM identity
@router.delete("/llm-identities/{id}", response_model=dict)
def delete_llm_identity(id: int, db: Session = Depends(get_db)):
    llm_identity = db.query(LLMIdentity).filter(LLMIdentity.id == id).first()
    if not llm_identity:
        raise HTTPException(status_code=404, detail="LLM Identity not found")

    db.delete(llm_identity)
    db.commit()

    return {"detail": "LLM Identity deleted"}

from dependencies import get_authenticated_user, Token

# GET /llm-identities/user/:user_id: Retrieve LLM identities for a specific user
@router.get("/llm-identities/user/{google_account_id}", response_model=List[LLMIdentityOut])
def get_llm_identities_by_user(google_account_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.google_account_id == google_account_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    llm_identities = db.query(LLMIdentity).filter(LLMIdentity.user_id == user.id).all()

    return llm_identities
