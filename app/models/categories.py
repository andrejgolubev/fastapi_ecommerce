# app/models/categories.py
from sqlalchemy import String, Boolean, ForeignKey
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.products import Product

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    
    products: Mapped[list["Product"]] = relationship(
        'Product',
        back_populates='category', 
        uselist=True
    )

    parent_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'), nullable=True)

    parent: Mapped[Optional["Category"]] = relationship(
        'Category',
        back_populates='children', 
        remote_side=[id],
        foreign_keys=[parent_id]
    )

    children: Mapped[list["Category"]] = relationship(
        'Category',
        back_populates='parent'
    )