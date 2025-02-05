from sqlalchemy.orm import Mapped
from sqlalchemy import Column, String
from sqlalchemy.orm import mapped_column
from domain.model.common import Base
from datetime import datetime
from dataclasses import dataclass 
from datetime import datetime

@dataclass
class Country(Base):
    """国家列表"""
    __tablename__ = "county"
    code: Mapped[str] = mapped_column(nullable=True,)
    name: Mapped[str] = mapped_column(nullable=True,)

@dataclass
class Region(Base):
    """行政区域"""
    __tablename__ = "regon"
    country_id: Mapped[str] = mapped_column(nullable=True,)
    code: Mapped[str] = mapped_column(nullable=True,)
    name: Mapped[str] = mapped_column(nullable=True,)

@dataclass
class School(Base):
    """区域所在学校"""
    __tablename__ = "school"
    region_id: Mapped[str] = mapped_column(nullable=True,)
    short_name: Mapped[str] = mapped_column(nullable=True,)
    full_name: Mapped[str] = mapped_column(nullable=True,)

@dataclass
class Person(Base):
    """个人信息"""
    __tablename__ = "person"
    first_name: Mapped[str] = mapped_column(nullable=True,)
    last_name: Mapped[str] = mapped_column(nullable=True,)
    full_name: Mapped[str] = mapped_column(nullable=True,)
    gender: Mapped[int] = mapped_column(nullable=True,default=0)
 
@dataclass
class Parent(Base):
    """家长信息"""
    __tablename__ = "parent"
    person_id: Mapped[str] = mapped_column(nullable=True,)
 
@dataclass
class Student(Base):
    """学生信息"""
    __tablename__ = "student"
    person_id: Mapped[str] = mapped_column(nullable=True,)
    grade: Mapped[int] = mapped_column(nullable=True,)
    school_id: Mapped[str] = mapped_column(nullable=True,)
    school_name: Mapped[str] = mapped_column(nullable=True,)
    parent_id: Mapped[str] = mapped_column(nullable=True,)
    access_code: Mapped[str] = mapped_column(nullable=True,)

@dataclass
class Account(Base):
    __tablename__ = "account"
    mobile: Mapped[str] = mapped_column(nullable=True,unique=True)
    parent_id: Mapped[str] = mapped_column(nullable=True,)
    register_time: Mapped[datetime] = mapped_column(nullable=True,default=datetime.now())