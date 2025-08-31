from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Session
from fastapi import FastAPI, APIRouter, Depends
from app.db_depends import get_db
from app.schemas import UserSchema
from app.models import UserModel 

router=APIRouter(tags=['user'], prefix='/')

class Base(DeclarativeBase):
    pass

@router.get('/', response_model=UserSchema, status_code=200)
async def get_all_users(db: Session = Depends(get_db)): 

    ...


