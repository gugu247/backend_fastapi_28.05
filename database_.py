from os.path import split

from schemas import Project, ProjectCreate, ProjectUpdate, Task,PeopleCreate,PeopleUpdate, People, Filter, ItogFilter, TaskCreate, TaskUpdate, \
    StatKolvo, StatKorzina, StatKorzinaInfo, UserProfile

import sqlite3
import os



from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(
    os.getenv('DATABASE_PATH', str(BASE_DIR / 'projects.db'))
)




def get_connection_pr():
    connection = sqlite3.connect(DATABASE_PATH)
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




# def get_connection_pr():
#     connection = sqlite3.connect('tasks.db')
#     connection.row_factory = sqlite3.Row
#     return connection

def create_table_task():
    with get_connection_pr() as connection:
        connection.execute(
            """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority INTEGER,
                    end_time TEXT NOT NULL,
                    proj_id INTEGER NOT NULL
                )
            """
        )



# def get_connection_pr():
#     connection = sqlite3.connect('peoples.db')
#     connection.row_factory = sqlite3.Row
#     return connection

def create_table_pl():
    with get_connection_pr() as connection:
        connection.execute(
            """
                CREATE TABLE IF NOT EXISTS peoples (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL DEFAULT [],
                    proj_id INTEGER NOT NULL
                )
            """
        )




def create_table_user():
    with get_connection_pr() as connection:
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
    end_time='2026-06-05',
    proj_id=1)

task2 = Task(
    id=2,
    title='June',
    description='50k',
    status='in_progress',
    priority=2,
    end_time='2026-07-01',
    proj_id=1)

task3 = Task(
    id=3,
    title='July',
    description='100k',
    status='new',
    priority=3,
    end_time='2026-08-01',
    proj_id=1)

task4 = Task(
    id=4,
    title='August',
    description='150k',
    status='new',
    priority=4,
    end_time='2026-09-01',
    proj_id=1)

tasks=[
    task1,task2,task3,task4
]

peoples = [People(id=1,name='Chel1',proj_id=1),People(id=2,name='Chel2',proj_id=1)]


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

proj2 = Project(
    id=2,
    title="Jobergerg",
    description="Zarabotsdefaftdsedf na leto",
    tasks=tasks,
    peoples=peoples,
    end_time="2026-09-01",
    status="NONONONOONONO")

projects = [
    proj1, proj2
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
        tmp_tasks = ""
        tmp_peoples = ''
        print(len(tasks))
        for project in projects:

            for task in tasks:
                str_tasks = ''
                str_tasks += str(task.id) + '|' + str(task.title) + '|' + str(task.description) + '|' + str(task.status) + '|' + str(task.priority) + '|' + str(task.end_time)
                tmp_tasks += str_tasks + "}"
            for people in peoples:
                str_peoples = ''
                str_peoples += str(people.id) + '|' + str(people.name)
                tmp_peoples += str_peoples + '}'

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
                    tmp_tasks,
                    str_peoples,
                    project.end_time,
                    project.status,
                )
            )
    
    with get_connection_pr() as connection:
        task_len = connection.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
        if task_len > 0:
            return "OK task is exist"
        else:
            for project in projects:

                for task in tasks:
                    connection.execute(
                        """
                        INSERT INTO tasks (
                            title,
                            description,
                            status,
                            priority,
                            end_time,
                            proj_id
                        )
                        VALUES (?,?,?,?,?,?)
                        """,
                        (
                            task.title,
                            task.description,
                            task.status,
                            task.priority,
                            task.end_time,
                            project.id
                        )
                    )
    
    with get_connection_pr() as connection:
        people_len = connection.execute('SELECT COUNT(*) FROM peoples').fetchone()[0]
        if people_len > 0:
            return "OK people is exist"
        else:
            for project in projects:
                for people in peoples:
                    connection.execute(
                        """
                        INSERT INTO peoples (
                            name,
                            proj_id
                        )
                        VALUES(?,?)
                        """,
                        (
                            people.name,
                            project.id
                        )
                    )


def row_project(row:sqlite3.Row) -> Project: #Переводим из формата sql в формат python
    return Project(
        id=int(row["id"]),
        title=row["title"],
        description=row["description"],
        tasks=row["tasks"],
        peoples=row["peoples"],
        end_time=row["end_time"],
        status=row["status"],
    )

def get_project() -> list[Project]:
    with get_connection_pr() as connection:
        rows = connection.execute("SELECT * FROM projects ORDER BY id").fetchall()
        list_temp = []
        for row in rows:
            tempProject = row_project(row)
            print(tempProject)
            list_temp.append(tempProject)
        return list_temp

def get_project_by_id(project_id: int) -> Project | None:
    with get_connection_pr() as connection:
        row = connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        return None
    print(row_project(row))
    return row_project(row)

def create_project(project: ProjectCreate) -> Project:
    with get_connection_pr() as connection:
        for task in tasks:
            str_tasks = ''
            str_tasks += str(task.id) + '|' + str(task.title) + '|' + str(task.description) + '|' + str(
                task.status) + '|' + str(task.priority) + '|' + str(task.end_time)

        for people in peoples:
            str_peoples = ''
            str_peoples += str(people.id) + '|' + str(people.name)

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
                str_tasks,
                str_peoples,
                project.end_time,
                project.status,
            )
        )
        project_id = int(cursor.lastrowid)
        row = connection.execute("""SELECT * FROM projects WHERE id= ?""",(project_id,)).fetchone()
        return row_project(row)

def update_project(project_id: int, project: ProjectUpdate) -> Project | None:
    updates = project.model_dump(exclude_unset=True)
    print(updates)
    izmen_fields = ('title','description','status') 
    with get_connection_pr() as connection:
        if connection.execute("""SELECT 1 FROM projects WHERE id=?""",(project_id,)).fetchone() is None:
            return None
        if updates:
            for key, value in updates.items(): #key - это izmen_fields, то есть ячейки таблицы
                print(key, value)
                connection.execute(f"UPDATE projects SET {key} = '{value}' WHERE id={project_id}")
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
    return Task(
        id=int(row["id"]),
        title=row["title"],
        description=row["description"],
        status=row["status"],
        priority=row["priority"],
        end_time=row["end_time"],
        proj_id=int(row["proj_id"])
    )
   
def get_task() -> list[Task]:
    with get_connection_pr() as connection:
        rows = connection.execute('SELECT * FROM tasks ORDER BY id').fetchall()
        list_temp = []
        for row in rows:
            tempTask = row_task(row)
            print(tempTask)
            list_temp.append(tempTask)
        return list_temp

def get_task_by_id(task_id:int) -> list[Task] | None:
    with get_connection_pr() as connection:
        rows = connection.execute('SELECT * FROM tasks WHERE proj_id=?',(task_id,)).fetchall()
        list_temp = []
        if rows is None:
            return None
        for row in rows:
            tempTask = row_task(row)
            print(tempTask)
            list_temp.append(tempTask)
        return list_temp

def create_task(task: TaskCreate, proj_id) -> Task:
    with get_connection_pr() as connection:
        for project in projects:
            if project.id == proj_id:

                cursor = connection.execute(
                    """
                    INSERT INTO tasks (
                        title,
                        description,
                        status,
                        priority,
                        end_time,
                        proj_id
                    )
                    VALUES (?,?,?,?,?,?)
                    """,
                    (
                        task.title,
                        task.description,
                        task.status,
                        task.priority,
                        task.end_time,
                        project.id
                    )
                )
                task_id = int(cursor.lastrowid)
                row = connection.execute("""SELECT * FROM tasks WHERE id= ?""",(task_id,)).fetchone()
                return row_task(row)

def update_task(task_id: int, task: TaskUpdate) -> Task | None:
    updates = task.model_dump(exclude_unset=True)
    izmen_fields = ('title','description','status') 
    with get_connection_pr() as connection:
        if connection.execute("""SELECT 1 FROM tasks WHERE id=?""",(task_id,)).fetchone() is None:
            return None
        if updates:
            for key, value in updates.items(): #key - это izmen_fields, то есть ячейки таблицы
                connection.execute(f"UPDATE tasks SET {key} = '{value}' WHERE id={task_id}")
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
        id=int(row['id']),
        name=row['name'],
        proj_id=int(row['proj_id'])
    )
    return newPeople

def get_people() -> list[People]:
    with get_connection_pr() as connection:
        rows = connection.execute('SELECT * FROM peoples').fetchall()
        list_tmp = []
        for row in rows:
            row_tmp = row_people(row)
            list_tmp.append(row_tmp)
        return list_tmp

def get_people_by_id(people_id:int) -> list[People] | None:
    with get_connection_pr() as connection:
        rows = connection.execute('SELECT * FROM peoples WHERE proj_id=?',(people_id,)).fetchall()
        list_temp = []
        if rows is None:
            return None
        for row in rows:
            tempPeople = row_people(row)
            print(tempPeople)
            list_temp.append(tempPeople)
        return list_temp
    
def create_people(proj_id:int, people: PeopleCreate) -> People:
    with get_connection_pr() as connection:
        for project in projects:
            if project.id == proj_id:
                cursor = connection.execute(
                    """
                    INSERT INTO peoples (
                        name,
                        proj_id
                    )
                    VALUES (?,?)
                    """,
                    (
                        people.name,
                        project.id
                    )
                )
                people_id = int(cursor.lastrowid)
                row = connection.execute("""SELECT * FROM peoples WHERE id= ?""",(people_id,)).fetchone()
                return row_people(row)

def update_people(people_id: int, people: PeopleUpdate) -> People | None:
    updates = people.model_dump(exclude_unset=True)
    izmen_fields = ('name') 
    with get_connection_pr() as connection:
        if connection.execute("""SELECT 1 FROM peoples WHERE id=?""",(people_id,)).fetchone() is None:
            return None
        if updates:
            for key, value in updates.items(): #key - это izmen_fields, то есть ячейки таблицы
                connection.execute(f"UPDATE peoples SET {key} = '{value}' WHERE id={people_id}")
        row = connection.execute("""SELECT * FROM peoples WHERE id=?""",(people_id,)).fetchone()
        return row_people(row)

def delete_people(people_id:int) -> bool:
    with get_connection_pr() as connection:
        cursor = connection.execute("DELETE FROM peoples WHERE id = ?",(people_id,))
        if cursor.rowcount > 0:
            return True
        else:
            return False




def row_user(row:sqlite3.Row) -> UserProfile:
    return UserProfile(
        id=int(row['id']),
        username=row['username'],
        role=row['role']
    )

def get_user_by_id(user_id:int) -> UserProfile | None:
    with get_connection_pr() as connection:
        row = connection.execute('SELECT * FROM users').fetchall()
        if row is None:
            return None
        tmp_list = []
        tmp_list2 = []
        for elem in row:
            tmp_list.append(elem)
            tmp_list2.append(elem['id'])
        for i in tmp_list2:
            if i == user_id - 1:
                for j in tmp_list:
                    if int(j['id']) == i:
                        print(row_user(j))
                        return row_user(j)
        # if row is None:
        #     return None
        # return row_user(row)

def get_user_record_by_username(username:str) -> int | None:
    with get_connection_pr() as connection:
        # row = connection.execute('SELECT * FROM users WHERE username=?',(username,)).fetchone()
        row = connection.execute('SELECT * FROM users').fetchall()
        tmp_list = []
        tmp_list2 = []
        for elem in row:
            tmp_list.append(elem['username'])
            tmp_list2.append(elem['id'])
        # print(username)
        # print(tmp_list)
        if username in tmp_list:
            return None
        return tmp_list2[-1]

def create_user(username:str,password_hash:str) -> UserProfile:
    with get_connection_pr() as connection:
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
        return user
