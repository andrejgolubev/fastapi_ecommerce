from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import SessionLocal


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
