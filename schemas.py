from pydantic import BaseModel



class StudentCreate(BaseModel):
    name:str
    age:int
    adress:str|None=None
    password:str
    cid:int|None=None

class CourseCreate(BaseModel):
    cname:str


class Login(BaseModel):
    name:str
    password:str