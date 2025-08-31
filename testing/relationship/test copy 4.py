from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped as m, mapped_column as mc, relationship
from sqlalchemy import String, ForeignKey, Text, Numeric

class Base(DeclarativeBase): ... 

class Category(Base): 
    __tablename__='categories'
    id: m[int] = mc(primary_key=True)
    name: m[str] = mc(String(50), nullable=False)

    product: m[List["Product"]] = relationship(back_populates='category', uselist=True)

class Product(Base): 
    __tablename__='products'
    id: m[int] = mc(primary_key=True)
    name: m[str] = mc(String(150), nullable=False)
    price: m[float] = mc(Numeric(10,2), nullable=False)
    category_id: m[int] = mc(ForeignKey('categories.id'), nullable=False)

    category: m["Category"] = relationship(back_populates='product', uselist=False)
    