from sqlalchemy.orm import DeclarativeBase, Mapped as m, mapped_column as mc, relationship
from sqlalchemy import Integer, String, ForeignKey, Text, Numeric, Table, Column
from datetime import datetime
class Base(DeclarativeBase): ... 

article_tags=Table(
    'article_tags',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id') ),
)

class Article(Base): 
    __tablename__ = 'articles'
    id: m[int] = mc(primary_key=True) 
    title: m[str] = mc(String(200), nullable=False) 
    content: m[str] = mc(Text, nullable=False) 

    tag: m[list["Tag"]] = relationship(back_populates='article', secondary=article_tags) 

class Tag(Base): 
    __tablename__='tags'
    id: m[int] = mc(primary_key=True) 
    name: m[str] = mc(String(50),unique=True,nullable=False) 

    article: m[list["Article"]] = relationship(back_populates='tag', secondary=article_tags) 