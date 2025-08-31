from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped as m, mapped_column as mc, relationship
from sqlalchemy import String, ForeignKey, Text, Numeric

class Base(DeclarativeBase): ... 

class Student(Base):
    __tablename__ = 'students'

    id: m[int] = mc(primary_key=True, unique=True)
    name: m[str] = mc(String(100) , nullable=False) 
    student_id: m[str] = mc(String(20), unique=True, nullable=False)

    grade: m[list["Grade"]] = relationship(
        back_populates='student'
    )

class Grade(Base): 
    __tablename__='grades'

    id: m[int] = mc(primary_key=True, unique=True)
    value: m[int] = mc(nullable=False)
    subject: m[str] = mc(String(50) , nullable=False)
    student_id: m[int] = mc(ForeignKey('students.id'), nullable=False)

    student: m["Student"] = relationship(
        back_populates='grade',

    )
      
