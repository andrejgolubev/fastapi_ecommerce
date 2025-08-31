from sqlalchemy import String
from sqlalchemy.orm import mapped_column as mc, Mapped, DeclarativeBase
from pydantic import BaseModel

class Base(DeclarativeBase): ...

class CategoryCreate(BaseModel):
    id: int
    name: str

class CategoryGet(BaseModel): 
    id: int 
    name:str 

class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mc(primary_key=True)
    name: Mapped[str] = mc(String(50), nullable=False)
    
