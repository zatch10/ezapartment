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


def duplicate_address(address):
    cur = db.connect()
    query = f" SELECT Address FROM Apartments WHERE Address = '{address}'"
    results = cur.execute(query)

    arr = []
    for row in results:
        arr.append(row)
    
    if len(arr) < 1:
        return False    
    return True

def insertApartment(array):
    cur = db.connect()
    for i in range(len(array)):
        if i == 2 or i == 3 or i == 7:
            if array[i] == "":
                array[i] = 0
            else:
                try:
                    array[i] = int(array[i])
                except:
                    return False

        if array[i] == "":
            array[i] = "N/A"
    
        
    query = f"INSERT INTO Apartments(Address, Complex_Name, Units, Stories, Building_Type, Street, Company, Rent) VALUES('{array[0]}', '{array[1]}', {array[2]}, {array[3]}, '{array[4]}', '{array[5]}', '{array[6]}', {array[7]})"
    cur.execute(query)
    return True

def searchApartment(address):
    cur = db.connect()
    query = f"SELECT * FROM Apartments WHERE Address = '{address}'"
    results = cur.execute(query)
    ans = []
    for row in results:
        ans.append(row)
    return ans

def updateApartment(field, update, address):
    cur = db.connect()
    try:
        for i in range(len(field)):
            query = f"UPDATE Apartments SET {field[i]} = '{update[i]}' WHERE Address = '{address}'"
            results = cur.execute(query)
        return True
    except Exception as e:
        print(e)
        return False

def deleteApartment(address):
    cur = db.connect()
    query = f"DELETE FROM Apartments WHERE Address = '{address}'"
    try:
        cur.execute(query)
    except:
        return False
    return True

def advQuery():
    query = "SELECT A.Address, A.Rent, B.Company, D.Complex_Name FROM (SELECT avg(Rent) as average from Apartments) as C, Apartments A NATURAL JOIN Amenities B Natural JOIN Included_Utilities D WHERE B.Gym = True AND A.Rent < C.average AND D.maintainance = True order by Rent ASC LIMIT 15;"
    cur = db.connect()
    results = cur.execute(query)
    ans = []
    for row in results:
        ans.append(row)
    return ans