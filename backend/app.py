from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, llm_identities, threads, messages

from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Set up CORS middleware
origins = [
    "http://localhost:3000",  # Adjust this to your frontend's development server URL
    "https://your-production-frontend-url.com",  # Replace this with your production frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(llm_identities.router)
app.include_router(threads.router)
app.include_router(messages.router)
