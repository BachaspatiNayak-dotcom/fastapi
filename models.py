from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import String,Integer,ForeignKey
from database import *

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__="students"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    age:Mapped[int]=mapped_column(Integer)
    adress:Mapped[str | None]=mapped_column(String(100),nullable=True)
    password:Mapped[str]=mapped_column(String(255),nullable=True)
    cid:Mapped[int]=mapped_column(ForeignKey("courses.id"),nullable=True)

    course=relationship("Course")



class Course(Base):
    __tablename__="courses"

    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    cname:Mapped[str]=mapped_column(String(30))



