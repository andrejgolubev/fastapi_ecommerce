from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped as m, mapped_column as mc, relationship
from sqlalchemy import String, ForeignKey, Text, Numeric

class Base(DeclarativeBase): ... 

class Customer(Base): 
    __tablename__ = 'customers'

    id: m[int] = mc(primary_key=True)
    name: m[str] = mc(String(100), nullable=False) 
    email: m[str] = mc(String(120), nullable=False, unique=True) 

    order: m[List["Order"]] = relationship(back_populates='customer', uselist=True)

class Order(Base): 
    __tablename__ = 'orders'

    id: m[int] = mc(primary_key=True)
    order_number : m[str] = mc(String(20), unique=True, nullable=False) 
    total_amount: m[float] = mc(Numeric(10,2), nullable=False)
    customer_id: m[int] = mc(ForeignKey('customers.id'), unique=True, nullable=False)

    customer: m["Customer"] = relationship(back_populates='order', uselist=False)