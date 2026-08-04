from http.client import HTTPException

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends
from pydantic import BaseModel, Field

import database_
from schemas import Project, ProjectCreate, ProjectUpdate, Task, People, Filter, ItogFilter, TaskCreate, TaskUpdate, \
    StatKolvo, StatKorzina, StatKorzinaInfo, UserProfile, UserCreate, Token
from database_ import projects, tasks, task_stat, kolvo_stat, count_stat
from database_ import get_project,get_project_by_id,get_people,get_people_by_id,get_task,get_task_by_id,create_project,create_task, \
create_people,update_project,update_task,update_people,delete_project,delete_task,delete_people

import auth
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

database_.create_table_pr()
database_.create_table_task()
database_.create_table_pl()
database_.create_table_user()

database_.zapoln_defaults()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'https://localhost:5500',
        'https://127.0.0.1:5500',
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)


@app.get("/")
def root():
    return {'message': 'GoalPlan'}


@app.get("/all-projects",response_model=list[Project])
def get_pr():
    return get_project()


@app.get('/projects/search')
def search_pr(query: str = Query(min_length=2)):
    query = query.lower()
    result = []
    projectsdb = get_project()
    for project in projectsdb:
        if project.title.lower() == query or project.description.lower() == query:
            result.append(project)
    return result


@app.get("/projects/{proj_id}")
def get_pr_id(proj_id: int):
    # for proj in projects:
    #     if proj.id == proj_id:
    #         return proj
    return get_project_by_id(proj_id)


@app.post("/projects")
def proj_create(proj_data: ProjectCreate):
    # id_next = projects[-1].id + 1
    # project = Project(id=id_next,
    #                   title=proj_data.title,
    #                   description=proj_data.description,
    #                   tasks=proj_data.tasks,
    #                   peoples=proj_data.peoples,
    #                   end_time=proj_data.end_time,
    #                   status=proj_data.status)
    return create_project(proj_data)


@app.patch("/projects/{proj_id}")
def proj_update(proj_id: int, proj_data: ProjectUpdate):
    # proj_ind = 0
    # for proj in projects:
    #     if proj.id == proj_id:
    #         projectupd = proj
    #         proj_ind = projects.index(proj)

    # if proj_ind == -1:
    #     return {'error': "Error"}

    # upd_data = proj_data.model_dump(exclude_unset=True)
    # upd_proj = projectupd | upd_data
    # projects[proj_ind] = upd_proj

    return update_project(proj_id,proj_data)


@app.delete("/projects/{proj_id}")
def del_pr(proj_id: int):
    # for proj in projects:
    #     if proj_id == proj.id:
    #         projects.remove(proj)
    # return {'ERROR': 'ERROR'}
    return delete_project(proj_id)






@app.get('/tasks')
def get_tasks():
    get_task()


@app.get('/tasks/{task_id}')
def get_task_id(task_id: int):
    # for task in tasks:
    #     if task.id == task_id:
    #         return task
    return get_task_by_id(task_id)


@app.post('/tasks')
def post_tasks(task_data: TaskCreate):
    # task = Task(
    #     id=tasks[-1].id + 1,
    #     title=task_data.title,
    #     description=task_data.description,
    #     status=task_data.status,
    #     priority=task_data.priority,
    #     end_time=task_data.end_time)
    return create_task(task_data)


@app.patch('/tasks/{task_id}')
def patch_task(task_id:int,task_data: TaskUpdate):
    # task_ind = 0
    # for task in tasks:
    #     if task.id == task_id:
    #         taskupd = task
    #         task_ind = tasks.index(task)

    # if task_ind == -1:
    #     return {'error': 'error'}

    # upd_data = task_data.model_dump(exclude_unset=True)
    # upd_task = taskupd | upd_data
    # tasks[task_ind] = upd_task

    return update_task(task_id,task_data)


@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    # for task in tasks:
    #     if task.id == task_id:
    #         tasks.remove(task)
    # return {'error': 'error'}
    return delete_task(task_id)


@app.get('/tasks/status/{status}')
def get_status(status: str):
    task_list_stat = []
    for task in tasks:
        if task.status == status:
            task_list_stat.append(task)
    return task_list_stat


@app.patch("/tasks/priority/{task_id}")
def priority_plus_one(task_id: int):
    for task in tasks:
        if task.id == task_id:
            if task.priority == 5:
                return {'error': 'error'}
            else:
                task.priority = task.priority + 1
                return {'ok': 'priority plus one'}


@app.get('/tasks/stat/{task_id}')
def stat(task_id: int):
    for task in tasks:
        if task.id == task_id:
            element_StatKorzina = StatKorzina(task_id=task_id)
            task_stat.append(element_StatKorzina)
            kolvo_stat.append(task)
            database_.count_stat += 1


def get_task_by_id_mainpy(task_id: int) -> StatKorzina | None:
    for task in task_stat:
        if task.task_id == task_id:
            return task
    return None


@app.post('/auth/register')
def register(user_data: UserCreate):
    if database_.get_user_record_by_username(user_data.username) is None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail='User с таким login уже есть'
        )
    return database_.create_user(
        username=user_data.username,
        password_hash=auth.hash_password(user_data.password)
    )


@app.post('/auth/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(
        form_data.username,
        form_data.password
    )
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль'
        )
    return Token(access_token=auth.create_access_token(user), token_type='bearer')

