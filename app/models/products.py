from sqlalchemy import String, Boolean, Float, Integer, ForeignKey
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


if TYPE_CHECKING: # Для аннотаций типов
    from app.models import User, Review, Category


class Product(Base):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(200), nullable=True)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)

    
    rating: Mapped[float] = mapped_column(nullable=True, default=None)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))

    seller_id: Mapped[str] = mapped_column(ForeignKey('users.id'), nullable=False)


    category: Mapped["Category"] = relationship(
        'Category',
        back_populates='products'
    )

    seller: Mapped["User"] = relationship(back_populates='products')

    review: Mapped[list['Review']] = relationship(back_populates='product')


