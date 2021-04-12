"""Defines all the functions related to the database"""
from app import db

def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from tasks;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2]
        }
        todo_list.append(item)

    return todo_list


def update_task_entry(task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(task_id: int, text: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into tasks (task, status) VALUES ("{}", "{}");'.format(
        text, "Todo")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From tasks where id={};'.format(task_id)
    conn.execute(query)
    conn.close()


def createUser(username, password):
    cur = db.connect()
    if fetchUser(username) is False:
        query = f"INSERT INTO users(username, password) VALUES('{username}', '{password}')"
        cur.execute(query)
        print("reached")
        return True
    return False

def validateUser(username, password):
    cur = db.connect()
    query = f"SELECT username, password FROM users WHERE username = '{username}'"
    results = cur.execute(query)
    arr = []
    for row in results:
        print(row)
        arr.append(row)
    if len(arr) <1:
        return False
    
    user_record = arr[0]
    user_password = user_record['password']

    if user_password == password:
        return True
    else:
        return False

def fetchUser(username):
    cur = db.connect()
    query = f" SELECT username FROM users WHERE username = '{username}'"
    results = cur.execute(query)
    # query = f" SELECT Street FROM security_index"
    # results = cur.execute(query)
    arr = []
    for row in results:
        print(row)
        arr.append(row)
    # print(results.keys)
    print(len(arr))
    if len(arr) < 1:
        return False    
    return True

def searchApartment(address):
    cur = db.connect()
    query = f"SELECT * FROM apartments WHERE Address = '{address}'"
    results = cur.execute(query)
    ans = []
    for row in results:
        ans.append(row)

    return ans[0]