from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Table
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    google_account_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    llm_identities = relationship("LLMIdentity", back_populates="user")

class LLMIdentity(Base):
    __tablename__ = "llm_identities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model_name = Column(String, index=True)
    model_id = Column(String, unique=True, index=True)
    api_token = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="llm_identities")
    threads = relationship("Thread", secondary="llm_identity_thread")

class Thread(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("Message", back_populates="thread")
    llm_identities = relationship("LLMIdentity", secondary="llm_identity_thread")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("threads.id"))
    llm_identity_id = Column(Integer, ForeignKey("llm_identities.id"))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    thread = relationship("Thread", back_populates="messages")
    llm_identity = relationship("LLMIdentity")

# Association table for LLMIdentity and Thread
llm_identity_thread = Table(
    "llm_identity_thread",
    Base.metadata,
    Column("llm_identity_id", Integer, ForeignKey("llm_identities.id"), primary_key=True),
    Column("thread_id", Integer, ForeignKey("threads.id"), primary_key=True)
)