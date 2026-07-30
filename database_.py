from schemas import Project, ProjectCreate, ProjectUpdate, Task,PeopleCreate,PeopleUpdate, People, Filter, ItogFilter, TaskCreate, TaskUpdate, \
    StatKolvo, StatKorzina, StatKorzinaInfo, UserProfile

import sqlite3


def get_connection_pr():
    connection = sqlite3.connect('projects.db')
    connection.row_factory = sqlite3.Row
    return connection

def create_table_pr():
    with get_connection_pr() as connection:
        connection.execute(
            """
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    tasks TEXT NOT NULL DEFAULT "[]",
                    peoples TEXT NOT NULL DEFAULT "[]",
                    end_time TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """
        )




def get_connection_task():
    connection = sqlite3.connect('tasks.db')
    connection.row_factory = sqlite3.Row
    return connection

def create_table_task():
    with get_connection_task() as connection:
        connection.execute(
            """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority INTEGER,
                    end_time TEXT NOT NULL
                )
            """
        )



def get_connection_pl():
    connection = sqlite3.connect('peoples.db')
    connection.row_factory = sqlite3.Row
    return connection

def create_table_pl():
    with get_connection_pl() as connection:
        connection.execute(
            """
                CREATE TABLE IF NOT EXISTS peoples (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL DEFAULT []
                )
            """
        )



def get_connection_user():
    connection = sqlite3.connect('users.db')
    connection.row_factory = sqlite3.Row
    return connection

def create_table_user():
    with get_connection_user() as connection:
        connection.execute(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'user',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
        )




task1 = Task(
    id=1,
    title='What is Job?',     
    description='Chto mne nuzhno ot raboti, kakaya nuzhna i t.d.',
    status='done',
    priority=1,
    end_time='2026-06-05')

task2 = Task(
    id=2,
    title='June',
    description='50k',
    status='in_progress',
    priority=2,
    end_time='2026-07-01')

task3 = Task(
    id=3,
    title='July',
    description='100k',
    status='new',
    priority=3,
    end_time='2026-08-01')

task4 = Task(
    id=4,
    title='August',
    description='150k',
    status='new',
    priority=4,
    end_time='2026-09-01')

tasks=[
    task1,task2,task3,task4
]

peoples = [People(id=1,name='Chel1'),People(id=2,name='Chel2')]


task_stat: list[StatKorzina] = []
kolvo_stat: list[StatKolvo] = []
count_stat = 0






proj1 = Project(
    id=1,
    title="Job",
    description="Zarabotat dengi na leto",
    tasks=tasks,
    peoples=peoples,
    end_time="2026-09-01",
    status="OK")

projects = [
    proj1,
]


filt1 = Filter(project_id=1, people=None)

filters = [
    filt1,
]



def zapoln_defaults():
    with get_connection_pr() as connection:
        projects_len = connection.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
        if projects_len > 0:
            return 'OK not null projects_len'
        for project in projects:
            connection.execute(
                """
                INSERT INTO projects (
                    title,
                    description,
                    tasks,
                    peoples,
                    end_time,
                    status
                )
                VALUES (?,?,?,?,?,?)
                """,
                (
                    project.title,
                    project.description,
                    project.tasks,
                    project.peoples,
                    project.end_time,
                    project.status,
                )
            )
    
    with get_connection_task() as connection:
        task_len = connection.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
        if task_len > 0:
            return "OK task is exist"
        else:
            for task in tasks:
                connection.execute(
                    """
                    INSERT INTO tasks (
                        title,
                        description,
                        status,
                        priority,
                        end_time
                    )
                    VALUES (?,?,?,?,?)
                    """,
                    (
                        task.title,
                        task.description,
                        task.status,
                        task.priority,
                        task.end_time,
                    )
                )
    
    with get_connection_pl() as connection:
        people_len = connection.execute('SELECT COUNT(*) FROM peoples').fetchone()[0]
        if people_len > 0:
            return "OK people is exist"
        else:
            for people in peoples:
                connection.execute(
                    """
                    INSERT INTO tasks (
                        name
                    )
                    VALUES(?)
                    """,
                    (
                        people.name
                    )
                )


def row_project(row:sqlite3.Row) -> Project: #Переводим из формата sql в формат python
    newProject = Project(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        tasks=row["tasks"],
        peoples=row["peoples"],
        end_time=row["end_time"],
        status=row["status"],
    )
    return newProject

def get_project() -> list[Project]:
    with get_connection_pr() as connection:
        rows = connection.execute("SELECT * FROM projects ORDER BY id").fetchall()
        list_temp = []
        for row in rows:
            tempProject = row_project(row)
            list_temp.append(tempProject)
        return list_temp

def get_project_by_id(project_id: int) -> Project | None:
    with get_connection_pr() as connection:
        row = connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        return None
    return row_project(row)

def create_project(project: ProjectCreate) -> Project:
    with get_connection_pr() as connection:
        cursor = connection.execute(
            """
            INSERT INTO projects (
                title,
                description,
                tasks,
                peoples,
                end_time,
                status
            )
            VALUES (?,?,?,?,?,?)
            """,
            (
                project.title,
                project.description,
                project.tasks,
                project.peoples,
                project.end_time,
                project.status,
            )
        )
        project_id = int(cursor.lastrowid)
        row = connection.execute("""SELECT * FROM projects WHERE id= ?""",(project_id,)).fetchone()
        return row_project(row)

def update_project(project_id: int, project: ProjectUpdate) -> Project | None:
    updates = project.model_dump(exclude_unset=True)
    izmen_fields = ('title','description','status') 
    with get_connection_pr() as connection:
        if connection.execute("""SELECT 1 FROM projects WHERE id=?""",(project_id,)).fetchone() is None:
            return None
        if updates:
            for key, value in updates: #key - это izmen_fields, то есть ячейки таблицы
                connection.execute(f"UPDATE projects SET {key} = {value} WHERE id={project_id}")
        row = connection.execute("""SELECT * FROM projects WHERE id=?""",(project_id,)).fetchone()
        return row_project(row)

def delete_project(project_id:int) -> bool:
    with get_connection_pr() as connection:
        cursor = connection.execute("DELETE FROM projects WHERE id = ?",(project_id,))
        if cursor.rowcount > 0:
            return True
        else:
            return False






def row_task(row:sqlite3.Row) -> Task: #Переводим из формата sql в формат python
    newTask = Task(
        id=row['id'],
        title=row['title'],
        description=row['description'],
        status=row['status'],
        priority=row['id'],
        end_time=row['end_time'],
    )
    return newTask

def get_task() -> list[Task]:
    with get_connection_task() as connection:
        rows = connection.execute('SELECT * FROM tasks ORDER BY id').fetchall()
        list_temp = []
        for row in rows:
            tempTask = row_task(row)
            list_temp(tempTask)
        return list_temp

def get_task_by_id(task_id:int) -> Task | None:
    with get_connection_task() as connection:
        row = connection.execute('SELECT * FROM tasks WHERE id=?',(task_id,)).fetchone()
    if row is None:
        return None
    return row_task(row)

def create_task(task: TaskCreate) -> Task:
    with get_connection_pr() as connection:
        cursor = connection.execute(
            """
            INSERT INTO projects (
                title,
                description,
                status,
                priority,
                end_time
            )
            VALUES (?,?,?,?,?)
            """,
            (
                task.title,
                task.description,
                task.status,
                task.priority,
                task.end_time
            )
        )
        task_id = int(cursor.lastrowid)
        row = connection.execute("""SELECT * FROM tasks WHERE id= ?""",(task_id,)).fetchone()
        return row_task(row)

def update_task(task_id: int, task: TaskUpdate) -> Task | None:
    updates = task.model_dump(exclude_unset=True)
    izmen_fields = ('title','description','status') 
    with get_connection_task() as connection:
        if connection.execute("""SELECT 1 FROM tasks WHERE id=?""",(task_id,)).fetchone() is None:
            return None
        if updates:
            for key, value in updates: #key - это izmen_fields, то есть ячейки таблицы
                connection.execute(f"UPDATE tasks SET {key} = {value} WHERE id={task_id}")
        row = connection.execute("""SELECT * FROM tasks WHERE id=?""",(task_id,)).fetchone()
        return row_task(row)

def delete_task(tasks_id:int) -> bool:
    with get_connection_pr() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?",(tasks_id,))
        if cursor.rowcount > 0:
            return True
        else:
            return False
        






def row_people(row:sqlite3.Row) -> People:
    newPeople = People(
        id=row['id'],
        name=row['id']
    )
    return newPeople

def get_people() -> list[People]:
    with get_connection_pl() as connection:
        rows = connection.execute('SELECT * FROM peoples').fetchall()
        list_tmp = []
        for row in rows:
            row_tmp = row_people(row)
            list_tmp.append(row_tmp)
        return list_tmp

def get_people_by_id(people_id:int) -> People | None:
    with get_connection_pl() as connection:
        row = connection.execute('SELECT * FROM peoples WHERE id=?',(people_id,)).fetchone()
        if row is None:
            return None
        return row_people(row)
    
def create_people(people: PeopleCreate) -> People:
    with get_connection_pl() as connection:
        cursor = connection.execute(
            """
            INSERT INTO projects (
                name
            )
            VALUES (?)
            """,
            (
                people.name
            )
        )
        people_id = int(cursor.lastrowid)
        row = connection.execute("""SELECT * FROM peoples WHERE id= ?""",(people_id,)).fetchone()
        return row_people(row)

def update_people(people_id: int, people: PeopleUpdate) -> People | None:
    updates = people.model_dump(exclude_unset=True)
    izmen_fields = ('name') 
    with get_connection_pl() as connection:
        if connection.execute("""SELECT 1 FROM peoples WHERE id=?""",(people_id,)).fetchone() is None:
            return None
        if updates:
            for key, value in updates: #key - это izmen_fields, то есть ячейки таблицы
                connection.execute(f"UPDATE peoples SET {key} = {value} WHERE id={people_id}")
        row = connection.execute("""SELECT * FROM peoples WHERE id=?""",(people_id,)).fetchone()
        return row_people(row)

def delete_people(people_id:int) -> bool:
    with get_connection_pl() as connection:
        cursor = connection.execute("DELETE FROM peoples WHERE id = ?",(people_id,))
        if cursor.rowcount > 0:
            return True
        else:
            return False




def row_user(row:sqlite3.Row) -> UserProfile:
    return UserProfile(
        id=row['id'],
        username=row['id'],
        role=row['id']
    )

def get_user_by_id(user_id:int) -> UserProfile | None:
    with get_connection_user() as connection:
        row = connection.execute('SELECT * FROM users WHERE id=?',(user_id,)).fetchone()
        if row is None:
            return None
        return row_user(row)

def get_user_record_by_username(username:str) -> sqlite3.Row | None:
    with get_connection_user() as connection:
        row = connection.execute('SELECT * FROM users WHERE username=?',(username,)).fetchone()
        if row is None:
            return None
        return row

def create_user(username:str,password_hash:str) -> UserProfile | None:
    with get_connection_user() as connection:
        cursor = connection.execute(
            """
                INSERT INTO users (
                    username,
                    password_hash
                )
                VALUES(?,?)
            """,
            (username,password_hash)
        )
        user_id = cursor.lastrowid
        user = get_user_by_id(user_id)
        if user is None:
            return None
        return user