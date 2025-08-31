from sqlalchemy.orm import DeclarativeBase, Mapped as m, mapped_column as mc, relationship
from sqlalchemy import String, ForeignKey
from typing import List

class Base(DeclarativeBase): ... 

class Author(Base):
    __tablename__='authors' 
    id: m[int] = mc(primary_key=True)
    name: m[str] = mc(String(100), nullable=False)

    book: m[List["Book"]] = relationship(back_populates='author', uselist=True)
    

class Book(Base): 
    __tablename__ = 'books'
    
    id: m[int] = mc(primary_key=True)
    title:m[str] = mc(String(200), nullable=False)
    author_id: m[int] = mc(ForeignKey('authors.id'), unique=True, nullable=False)

    author: m["Author"] = relationship(back_populates='book')
