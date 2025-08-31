from sqlalchemy.orm import DeclarativeBase, Mapped as m, mapped_column as mc, relationship
from sqlalchemy import String, ForeignKey, Text, Numeric
from datetime import datetime
class Base(DeclarativeBase): ... 

class Post(Base): 
    __tablename__='posts'
    id: m[int] = mc(primary_key=True)
    title: m[str] = mc(String(200), nullable=False)
    content: m[str] = mc(Text, nullable=False)
    created_at: m[datetime] = mc(nullable=False, default=datetime.now)    

    comment: m[list["Comment"]] = relationship(back_populates='post')

class Comment(Base): 
    __tablename__='comments'
    customersid : m[int] = mc(primary_key=True)
    content: m[str] = mc(Text,nullable=False)
    created_at: m[datetime] = mc(nullable=False, default=datetime.now)
    post_id: m[int] = mc(ForeignKey('posts.id'), nullable=False)

    post: m["Post"] = relationship(back_populates='comment')