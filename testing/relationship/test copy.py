from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# Модель пользователя
class User(Base):
    # Имя таблицы в базе данных
    __tablename__ = "users"
    
    # Первичный ключ, целое число, автогенерируемое
    id = Column(Integer, primary_key=True)
    
    # Имя пользователя, строка до 50 символов, уникальное и обязательное
    username = Column(String(50), unique=True, nullable=False)
    
    # Связь один-ко-многим, возвращает список объектов Order
    orders = relationship(
        "Order",                     # Имя связанной модели
        back_populates="user",       # Имя атрибута обратной связи в Order
        cascade="all, delete-orphan" # Удаляет заказы при удалении пользователя
    )

# Модель заказа
class Order(Base):
    # Имя таблицы в базе данных
    __tablename__ = "orders"
    
    # Первичный ключ заказа
    id = Column(Integer, primary_key=True)
    
    # Дата создания заказа, по умолчанию текущая дата и время
    order_date = Column(DateTime, default=datetime.now)
    
    # Сумма заказа, десятичное число с 2 знаками, обязательное
    total = Column(Numeric(10, 2), nullable=False)
    
    # Внешний ключ на users.id, обязательный
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Обратная связь с пользователем, возвращает одиночный объект User
    user = relationship(
        "User",                    # Имя связанной модели
        back_populates="orders"    # Имя атрибута обратной связи в User
    )
