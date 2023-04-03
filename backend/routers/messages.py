from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from datetime import datetime
from database import get_db
from models import Message, Thread, LLMIdentity

router = APIRouter()

class MessageCreate(BaseModel):
    thread_id: int
    llm_identity_id: int
    content: str

class MessageOut(BaseModel):
    id: int
    thread_id: int
    llm_identity_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# POST /messages: Create a new message
@router.post("/messages", response_model=MessageOut)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    # Check if the thread exists
    thread = db.query(Thread).filter(Thread.id == message.thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    # Check if the LLM identity exists
    llm_identity = db.query(LLMIdentity).filter(LLMIdentity.id == message.llm_identity_id).first()
    if not llm_identity:
        raise HTTPException(status_code=404, detail="LLM Identity not found")

    # Create a new message
    new_message = Message(**message.dict())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return MessageOut.from_orm(new_message)


# GET /threads/:id/messages: Retrieve all messages for a thread
@router.get("/threads/{thread_id}/messages", response_model=List[MessageOut])
def get_messages_for_thread(thread_id: int, db: Session = Depends(get_db)):
    # Check if the thread exists
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    # Get all messages for the thread
    messages = db.query(Message).filter(Message.thread_id == thread_id).all()
    return [MessageOut.from_orm(message) for message in messages]
