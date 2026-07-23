from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=2,max_length=80)
    description: str = Field(min_length=1,max_length=300)
    status: str = Field(min_length=1,max_length=15)
    priority: int = Field(ge=1,le=5)
    end_time: str = Field(min_length=10,max_length=10)

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None,min_length=2,max_length=80)
    description: str | None = Field(default=None,min_length=1,max_length=300)
    status: str | None = Field(default=None,min_length=1,max_length=15)
    priority: int | None = Field(default=None,ge=1,le=5)
    end_time: str | None = Field(default=None,min_length=10,max_length=10)



class Task(TaskCreate):
    id: int



class StatKorzina(BaseModel):
    task_id: int

class StatKorzinaInfo(BaseModel):
    task: Task

class StatKolvo(BaseModel):
    id: int
    tasks: list[StatKorzinaInfo]




class PeopleCreate(BaseModel):
    name: str = Field(min_length=2,max_length=80)

class PeopleUpdate(BaseModel):
    name: str | None = Field(default=None,min_length=2,max_length=80)

class People(PeopleCreate):
    id: int






class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: str
    tasks: list[Task]
    peoples: list[People]
    end_time: str
    status: str

class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None)
    tasks: Task | None = Field(default=None)
    peoples: People | None = Field(default=None)
    end_time: str | None = Field(default=None)
    status: str | None = Field(default=None)

class Project(ProjectCreate):
    id: int





class Filter(BaseModel):
    project_id: int | None = Field(default=None)
    people: str | None = Field(default= None)

class ItogFilter(Filter):
    id: int
    colichestvo: int





class UserCreate(BaseModel):
    username: str = Field(min_length=2,max_length=80)
    password: str = Field(min_length=2,max_length=80)

class UserProfile(BaseModel):
    id: int 
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str