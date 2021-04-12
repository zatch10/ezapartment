""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper
import flask

@app.route("/apartment_create", methods=['POST'])
def apartment_create():
    text = request.form['text']
    parsed = text.split(",")
    if(len(parsed) != 8):
        result = {'success': 0}
    else:
        result = {'success': 1}
    return jsonify(result)


@app.route("/apartment_read", methods=['POST'])
def apartment_read():
    text = request.form['text']
    search = db_helper.searchApartment(text)
    result = {'search' : search}
    return jsonify(result)





@app.route("/createuser", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    print("entering the create function")
    username = request.form['username']
    password = request.form['password']
    if db_helper.createUser(username, password): 
        return render_template("homepage.html")
    return render_template("Error.html")

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if db_helper.fetchUser(username) != None:
        if(db_helper.validateUser(username, password)):
            return flask.redirect("/homepage")

    return flask.redirect("/Error")

@app.route("/Error")
def error_page():
    print("reached error")
    return render_template("Error.html")


@app.route("/homepage")
def homepage():
    print("reached error")
    return render_template("homepage.html")


@app.route("/")
def start():
    """ returns rendered homepage """
    # items = db_helper.fetch_todo()
    return render_template("apartment.html")