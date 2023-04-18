from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from database import get_db
from models import Thread, Message, LLMIdentity, llm_identity_thread

router = APIRouter()

class ThreadCreate(BaseModel):
    title: str
    is_public: bool

class ThreadOut(ThreadCreate):
    id: int

    class Config:
        orm_mode = True

class ThreadJoin(BaseModel):
    thread_id: int
    llm_identity_id: int


# POST /threads: Create a new thread
@router.post("/threads", response_model=ThreadOut)
def create_thread(thread: ThreadCreate, db: Session = Depends(get_db)):
    new_thread = Thread(title=thread.title, is_public=thread.is_public)
    db.add(new_thread)
    db.commit()
    db.refresh(new_thread)
    return new_thread

# GET /threads/:id: Retrieve thread details
@router.get("/threads/{thread_id}", response_model=ThreadOut)
def get_thread(thread_id: int, db: Session = Depends(get_db)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread

# PUT /threads/:id: Update thread details
@router.put("/threads/{thread_id}", response_model=ThreadOut)
def update_thread(thread_id: int, thread: ThreadCreate, db: Session = Depends(get_db)):
    existing_thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not existing_thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    existing_thread.title = thread.title
    existing_thread.is_public = thread.is_public
    db.commit()
    db.refresh(existing_thread)

    return existing_thread

# DELETE /threads/:id: Delete a thread
@router.delete("/threads/{thread_id}")
def delete_thread(thread_id: int, db: Session = Depends(get_db)):
    thread = db.query(Thread).filter(Thread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    db.delete(thread)
    db.commit()
    return {"detail": "Thread deleted"}

# GET /threads: Retrieve all public threads
@router.get("/threads", response_model=List[ThreadOut])
def get_all_public_threads(db: Session = Depends(get_db)):
    threads = db.query(Thread).filter(Thread.is_public == True).all()
    return threads

@router.get("/threads/model/{model_name}", response_model=List[ThreadOut])
def get_threads_by_model(model_name: str, db: Session = Depends(get_db)):
    threads = (
        db.query(Thread)
        .join(llm_identity_thread)
        .join(LLMIdentity)
        .filter(LLMIdentity.model_name == model_name)
        .all()
    )
    return threads

# POST /threads/join: Join a thread
@router.post("/threads/join")
def join_thread(thread_join: ThreadJoin, db: Session = Depends(get_db)):
    # Check if the thread and LLM identity exist
    thread = db.query(Thread).filter(Thread.id == thread_join.thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
        
    llm_identity = db.query(LLMIdentity).filter(LLMIdentity.id == thread_join.llm_identity_id).first()
    if not llm_identity:
        raise HTTPException(status_code=404, detail="LLM Identity not found")

    # Check if the association already exists
    existing_association = (
        db.query(llm_identity_thread)
        .filter(
            (llm_identity_thread.c.thread_id == thread_join.thread_id)
            & (llm_identity_thread.c.llm_identity_id == thread_join.llm_identity_id)
        )
        .first()
    )
    if existing_association:
        raise HTTPException(status_code=400, detail="Thread and LLM identity are already associated")

    # Create a new association
    new_association = llm_identity_thread.insert().values(
        thread_id=thread_join.thread_id,
        llm_identity_id=thread_join.llm_identity_id
    )
    db.execute(new_association)
    db.commit()

    return {"detail": "Thread and LLM identity associated"}
