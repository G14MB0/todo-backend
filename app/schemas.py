from typing import Optional
import json

from pydantic import BaseModel, EmailStr #used as an isistance() to check data type
from datetime import datetime


######################################################
##              USER OPERATION TOKEN                ##
######################################################  

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str]


class UserUpdate(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    name: Optional[str]
    role: Optional[str]


class UserResponse(BaseModel):
    created_at: datetime
    email: EmailStr
    name: str
    id: int
    role: str
    created_at: datetime
    class Config:
        orm_mode = True


######################################################
##             LOGIN OPERATION SCHEMAS              ##
######################################################

class UserLogin(UserCreate):
    id: Optional[int]
    class Config:
        orm_mode = True
    # pass



######################################################
##             TOKEN OPERATION SCHEMAS              ##
######################################################

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None




######################################################
##           To-Do OPERATION SCHEMAS                 ##
######################################################

class TodoCreate(BaseModel):
    text: str
    dueDate: datetime


class TodoResponse(TodoCreate):
    id: int
    done: bool
    important: bool
    owner_id: int
    created_at: datetime


class TodoToggleDone(BaseModel):
    id: int
    

class TodoToggleImportant(BaseModel):
    id: int


class TodoDelete(BaseModel):
    id: int

