"""Defines all the functions related to the database"""
from app import db

def createUser(username, password):
    cur = db.connect()
    if fetchUser(username) is False:
        query = f"INSERT INTO users(username, password) VALUES('{username}', '{password}')"
        cur.execute(query)
        return True
    return False

def validateUser(username, password):
    cur = db.connect()
    query = f"SELECT username, password FROM users WHERE username = '{username}'"
    results = cur.execute(query)
    arr = []
    for row in results:
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
        arr.append(row)
    # print(results.keys)
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
            if field[i] == "Rent" or field[i] == "Stories" or field[i] == "Units":
                query = f"UPDATE Apartments SET {field[i]} = {update[i]} WHERE Address = '{address}'"
                results = cur.execute(query)
                continue
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