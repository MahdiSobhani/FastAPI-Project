from pydantic import BaseModel,Field

class UserCreate(BaseModel):
    username:str=Field(min_length=3,max_length=50)
    password:str=Field(min_length=6,max_length=100)

class Token(BaseModel):
    access_token:str
    token_type:str

class TaskCreate(BaseModel):
    title:str=Field(min_length=1,max_length=200)

class TaskUpdate(BaseModel):
    title:str|None=Field(default=None,min_length=1,max_length=200)
    completed:bool|None=None

class TaskResponse(BaseModel):
    id:int
    title:str
    completed:bool