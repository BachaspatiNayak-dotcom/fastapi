from fastapi import FastAPI,Depends,HTTPException
from pwdlib import PasswordHash
import jwt
import secrets
from dotenv import load_dotenv
import os
from fastapi.security import HTTPBearer
from datetime import datetime,timedelta,timezone
from models import Base,Student,Course
from schemas import StudentCreate,CourseCreate,Login
from database import SessionLocal,engine

app=FastAPI()

@app.get('/')
def sample():
    return "welcome to my FastAPI application"


# Base.metadata.create_all(engine)   #creating a non existent database table

password_hash=PasswordHash.recommended()

"""getting values from .env file"""
load_dotenv() 

"""getting the token value from bearer"""

security=HTTPBearer()

def get_db():   #creating a session for every request
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(credentials=Depends(security)):

    token=credentials.credentials

    payload=jwt.decode(
            token,
            SECURITY_KEY,
            algorithms=[ALGORITHM]
    )

    user_id=payload["id"]

    return user_id

@app.get("/student/")
def student_details(db=Depends(get_db),user_id=Depends(get_current_user)):
    print(db.query(Student))

    if user_id!=9:
        raise HTTPException(
            status_code=403,
            detail="you are not allowed to view student details"
        )
    students=db.query(Student).all()
    # students=db.query(Student).order_by(Student.id.asc()).all()
    # students=db.query(Student).filter(Student.age==25).all()
    # students=db.query(Student).filter(Student.name=="Isha").all()
    # students=db.query(Student).filter(Student.cid==2).all()

    return students


@app.post("/create_student")
def add_student(student:StudentCreate,db=Depends(get_db)):

    hashed_pw=password_hash.hash(student.password)

    db_student=Student(
        name=student.name,
        age=student.age,
        adress=student.adress,
        password=hashed_pw,
        cid=student.cid
    )
    db.add(db_student)
    db.commit()
    return "student created successfully"

@app.put("/update_student/{id}")
def update_student(id:int,student:StudentCreate,db=Depends(get_db)):
    db_student=db.query(Student).filter(Student.id==id).first()

    if db_student is None:
        return "student not found"

    hashed_password=password_hash.hash(student.password)

    db_student.name=student.name
    db_student.age=student.age
    db_student.adress=student.adress
    db_student.password=hashed_password
    db_student.cid=student.cid

    db.commit()

    return "student updated successfully"


@app.delete("/del_student/{id}")
def del_student(id:int,db=Depends(get_db)):
    db_student=db.get(Student,id)

    if db_student is None:
        return "there is no student with such id"
    
    db.delete(db_student)
    db.commit()

    return "student deleted successfully"

@app.post("/add_course/")
def add_course(course:CourseCreate,db=Depends(get_db)):

    db_course=Course(
        cname=course.cname
    )
    db.add(db_course)
    db.commit()

    return "course craeted succesfully"



"""creating login and authentication functionality"""

SECURITY_KEY=os.getenv("SECURITY_KEY")
ALGORITHM="HS256"     #payload+SK+algo creates the signature for JWT


@app.post("/login/")
def login(data:Login,db=Depends(get_db)):

    db_student=db.query(Student).filter(
        Student.name==data.name
    ).first()

    if db_student is None:
        return "invalid username"

    if not password_hash.verify(data.password,db_student.password):
        return "wrong passsword"

    payload={
        "id":db_student.id,
        "name":db_student.name,
        "age":db_student.age,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=10)
    }

    token=jwt.encode(payload,SECURITY_KEY,algorithm=ALGORITHM)

    return {"message":"login successful","access_token":token}







     