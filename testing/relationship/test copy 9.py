from sqlalchemy.orm import DeclarativeBase, Mapped as m, mapped_column as mc, relationship
from sqlalchemy import Integer, String, ForeignKey, Text, Numeric, Table, Column
from datetime import datetime, date
class Base(DeclarativeBase): ... 


class Participation(Base): # Mapped Class (Association Object) 
    __tablename__ = 'participations'
    project_id: m[int] = mc(ForeignKey('projects.id'), primary_key=True) 
    employee_id: m[int] = mc(ForeignKey('employees.id'), primary_key=True)
    role: m[str] = mc(String(50), nullable=False)
    
    project: m["Project"] = relationship(back_populates="participations")
    employee: m["Employee"] = relationship(back_populates="participations")


class Project(Base): 
    __tablename__='projects'
    id: m[int] = mc(primary_key=True)
    name: m[str] = mc(String(150), nullable=False) 
    start_date: m[date] = mc(nullable=False)

    participations: m[list["Participation"]] = relationship(
        back_populates='project',
    )

    # employees: m[list["Employee"]] = relationship(
    #     secondary='participations',
    #     back_populates="projects",
    # )

class Employee(Base): 
    __tablename__='employees'
    id: m[int] =mc(primary_key=True)
    name: m[str] = mc(String(100), nullable=False) 
    email: m[str] = mc(String(120), nullable=False, unique=True)

    participations: m[list["Participation"]] = relationship(
        back_populates='employee', 

    )

    # projects: m[list["Project"]] = relationship(
    #     secondary='participations',
    #     back_populates='employees',
    # ) 