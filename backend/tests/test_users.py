from fastapi.testclient import TestClient
from app import app
from models import User
from database import SessionLocal

client = TestClient(app)

def test_create_user():
    test_user = {
        "google_account_id": "test_create_user_google_account_id",
        "email": "test_create_user@example.com"
    }

    response = client.post("/users", json=test_user)
    assert response.status_code == 201
    assert response.json()["google_account_id"] == test_user["google_account_id"]
    assert response.json()["email"] == test_user["email"]

    # Clean up the test user from the database
    db = SessionLocal()
    user = db.query(User).filter(User.google_account_id == test_user["google_account_id"]).first()
    db.delete(user)
    db.commit()
