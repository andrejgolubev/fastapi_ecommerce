from sqlalchemy import String, Boolean, Float, Integer, ForeignKey, Text
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import datetime
if TYPE_CHECKING: # Для аннотаций типов
    from .categories import Category
    from app.models import User, Product


class Review(Base): 
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(default=datetime.now) 
    grade: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)   

    user: Mapped['User'] = relationship(back_populates='review')
    product: Mapped['Product'] = relationship(back_populates='review')
