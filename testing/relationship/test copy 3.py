from sqlalchemy.orm import DeclarativeBase, Mapped as m, mapped_column as mc, relationship
from sqlalchemy import String, ForeignKey, Text

class Base(DeclarativeBase): ... 

class User(Base): 
    __tablename__='users'
    id: m[int] = mc(primary_key=True)
    username: m[str] = mc(String(50), nullable=False, unique=True)

    profile: m["Profile"] = relationship(back_populates='user', uselist=False)


class Profile(Base): 
    __tablename__='profiles'
    id: m[int] = mc(primary_key=True) 
    user_id: m[int] = mc(ForeignKey('users.id'), unique=True, nullable=False)
    bio: m[str] = mc(Text, nullable=True)

    user: m["User"] = relationship(back_populates='profile', uselist=False)