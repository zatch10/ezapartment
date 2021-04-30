""" Specifies routing for the application"""
from flask import render_template, request, jsonify, redirect, url_for
from app import app
from app import database as db_helper
import flask
import copy

@app.route("/apartment_create", methods=['POST'])
def apartment_create():
    text = request.form['text']
    parsed = text.split(",")
    
    if(db_helper.duplicate_address(parsed[0])):
        result = {'success': 0, 'error': "address exists"}

    elif(len(parsed) != 8):
        result = {'success': 0, 'error': "incorrect length"}
       
    elif(db_helper.insertApartment(parsed)):
        result = {'success': 1}
        
    else:
        result = {'success': 0, 'error': "int failure"}  

    return jsonify(result)


@app.route("/apartment_read", methods=['POST'])
def apartment_read():
    text = request.form['text']
    print(text)
    search = db_helper.searchApartment(text)
    result = {'search' : search}
    return jsonify(result)

@app.route("/apartment_update", methods=['POST'])
def apartment_update():
    field = request.form['field']
    update = request.form['update']
    address = request.form['address']
    field = field.split(",")
    update = update.split(",")
    if len(field) != len(update):
        result = {'success': 1}
        return jsonify(result)
    if(db_helper.updateApartment(field, update, address)):
        result = {'success': 1}
    else:
        result = {'success': 0}
    return jsonify(result)

@app.route("/apartment_delete", methods=['POST'])
def apartment_delete():
    text = request.form['text']
    if(not db_helper.duplicate_address(text)):
        result = {'success': 0}
        return jsonify(result)
    if(db_helper.deleteApartment(text)):
        result = {'success': 1}
    else:
        result = {'success': 0}
    return jsonify(result)

@app.route("/apartment_adv", methods=['POST'])
def apartment_adv():
    result = db_helper.advQuery()
    return jsonify(result)



@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    username = request.form['username']
    password = request.form['password']
    if db_helper.createUser(username, password):
        result = {'success':1}
    else:
        result = {'success':0}
    return jsonify(result)


@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if db_helper.validateUser(username, password):
        result = {'success':1}
    else:
        result = {'success':0}
    print("reached")
    return jsonify(result)

@app.route("/search", methods=['POST'])
def search():
    map = dict(request.form)
    temp = copy.deepcopy(map)  
    for Key in map:
        if Key == "min" and map[Key] == '':
            temp[Key] = 300
            map[Key] = 300
        if Key == "max" and map[Key] == '':
            temp[Key] = 2000
            map[Key] = 2000
        if map[Key] == '' or map[Key] == '0':
            temp.pop(Key)
        elif Key == 'Street':
            check = db_helper.checkStreet(map[Key])
            if check != False:
                temp[Key] = check[0]
                    # tmp = str()
                    # tmp += 
                    # for i in range(len(check)):
                    #     tmp += i
                    #     tmp += "OR"   
        # elif Key == "min" or Key == "max":

    test = str()
    check = 1
    for Key in temp:
        if (Key == "min" or Key == "max") and check:
            test += f"Rent >= {temp['min']} AND Rent <= {temp['max']} AND "
            check = 0
        elif Key != "min" and Key != "max":
            test += f"{Key} = '{temp[Key]}' AND "
    test = test[:-4]
    ans = db_helper.search(test)
    val = []
    
    if ans != False:
        for i in ans:
            map = {}
            map["Address"] = i[0]
            map["Rent"] = str(i[1])
            val.append(map)
    else:
        val = "No apartments found"
    result = {'search' : val} 
    return jsonify(result)

@app.route("/Error")
def error_page():
    print("reached error")
    return render_template("Error.html")


@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/apartment")
def apartment():
    return render_template("apartment.html")

@app.route("/included_utilities")
def included_utilities():
    return render_template("inlcuded_utilities.html")

@app.route("/amenities")
def amenities():
    return render_template("amenities.html")

@app.route("/Security_Index")
def Security_Index():
    return render_template("Security_Index.html")

@app.route("/")
def start():
    """ returns rendered homepage """
    # items = db_helper.fetch_todo()
    return render_template("login.html")

@app.route("/included_utilities_create", methods=['POST'])
def included_utilities_create():
    text = request.form['text']
    parsed = text.split(",")
    
    if(db_helper.duplicate_Complex_Name(parsed[0])):
        result = {'success': 0, 'error': "Company exists"}

    elif(len(parsed) != 5):
        result = {'success': 0, 'error': "incorrect length"}
       
    elif(db_helper.insertUtilities(parsed)):
        result = {'success': 1}
        
    else:
        result = {'success': 0, 'error': "int failure"}  

    return jsonify(result)


@app.route("/included_utilities_read", methods=['POST'])
def included_utilities_read():
    text = request.form['text']
    # print(text)
    search = db_helper.searchComplex_Name(text)
    result = {'search' : [dict(row) for row in search]}
    return jsonify(result)

@app.route("/included_utilities_update", methods=['POST'])
def included_utilities_update():
    field = request.form['field']
    update = request.form['update']
    company = request.form['company']
    field = field.split(",")
    update = update.split(",")
    if(db_helper.updateUtilities(field, update, company)):
        result = {'success': 1}
    else:
        result = {'success': 0}
    return jsonify(result)

@app.route("/included_utilities_delete", methods=['POST'])
def included_utilities_delete():
    text = request.form['text']
    if(not db_helper.duplicate_Complex_Name(text)):
       result = {'success': 0}
       return jsonify(result)
    if(db_helper.deleteComplex_Name(text)):
        result = {'success': 1}
    else:
        result = {'success': 0}
    return jsonify(result)

@app.route("/amenities_create", methods=['POST'])
def amenities_create():
    text = request.form['text']
    parsed = text.split(",")
    
    if(db_helper.duplicate_company(parsed[0])):
        result = {'success': 0, 'error': "Company exists"}

    elif(len(parsed) != 4):
        result = {'success': 0, 'error': "incorrect length"}
       
    elif(db_helper.insertAmenities(parsed)):
        result = {'success': 1}
        
    else:
        result = {'success': 0, 'error': "int failure"}  

    return jsonify(result)


@app.route("/amenities_read", methods=['POST'])
def amenities_read():
    text = request.form['text']
    # print(text)
    search = db_helper.searchCompany(text)
    result = {'search' : [dict(row) for row in search]}
    return jsonify(result)

@app.route("/amenities_update", methods=['POST'])
def amenities_update():
    field = request.form['field']
    update = request.form['update']
    company = request.form['company']
    field = field.split(",")
    update = update.split(",")
    if(db_helper.updateAmenities(field, update, company)):
        result = {'success': 1}
    else:
        result = {'success': 0}
    return jsonify(result)

@app.route("/amenities_delete", methods=['POST'])
def amenities_delete():
    text = request.form['text']
    if(not db_helper.duplicate_company(text)):
        result = {'success': 0}
        return jsonify(result)
    if(db_helper.deleteCompany(text)):
        result = {'success': 1}
    else:
        result = {'success': 0}
    return jsonify(result)

@app.route("/security_index_create", methods=['POST'])
def security_index_create():
    text = request.form['text']
    parsed = text.split(",")
    
    if(db_helper.duplicate_street(parsed[0])):
        result = {'success': 0, 'error': "Company exists"}

    elif(len(parsed) != 2):
        result = {'success': 0, 'error': "incorrect length"}
       
    elif(db_helper.insert_security_index(parsed)):
        result = {'success': 1}
        
    else:
        result = {'success': 0, 'error': "int failure"}  

    return jsonify(result)


@app.route("/security_index_read", methods=['POST'])
def security_index_read():
    text = request.form['text']
    # print(text)
    search = db_helper.search_street(text)
    result = {'search' : [dict(row) for row in search]}
    return jsonify(result)

@app.route("/security_index_update", methods=['POST'])
def security_index_update():
    field = request.form['field']
    update = request.form['update']
    company = request.form['company']
    field = field.split(",")
    update = update.split(",")
    if(db_helper.updateSecurity_Index(field, update, company)):
        result = {'success': 1}
    else:
        result = {'success': 0}
    return jsonify(result)

@app.route("/security_index_delete", methods=['POST'])
def security_index_delete():
    text = request.form['text']
    if(not db_helper.duplicate_street(text)):
       result = {'success': 0}
       return jsonify(result)
    if(db_helper.deleteStreet(text)):
        result = {'success': 1}
    else:
        result = {'success': 0}
    return jsonify(result)


@app.route("/recommend", methods=['POST'])
def recommend():
    val = request.form['val']
    address = db_helper.storedProcedure(val)
    print(address)
    val = []
    for i in address:
        map = {}
        map["Address"] = i[0]
        map["Rent"] = str(i[1])
        val.append(map)
    print(val)
    result = {'success' : val}
    return jsonify(result)