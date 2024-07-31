import multiprocessing
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, current_app, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import urllib.parse
from flask_cors import CORS
import importlib
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todolist.db"
app.config["SECRET_KEY"] = "mysecretkey"
db = SQLAlchemy(app)
CORS(app)

TODO_API_URL = "http://127.0.0.1:5001"
api_process = None


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    what_to_do = db.Column(db.String(100))
    due_date = db.Column(db.String(100))
    status = db.Column(db.String(100))


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "student" or request.form["password"] != "student":
            error = "Invalid credentials. Please try again."
        else:
            session["logged_in"] = True
            return redirect(url_for("show_list"))
    return render_template("login.html", error=error)


@app.route("/todo", methods=["GET", "POST"])
def show_list():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    response = requests.get(TODO_API_URL + "/api/items")
    items = response.json()
    return render_template("index-2.html", items=items)


@app.route("/add", methods=["POST"])
def add_entry():
    data = {"what_to_do": request.form["what_to_do"],
            "due_date": request.form["due_date"],
            "status": "open"}
    response = requests.post(TODO_API_URL + "/api/items", json=data)
    if response.status_code != 201:
        flash("Failed to add item!", "error")
    return redirect(url_for("show_list"))


@app.route("/mark/<item>")
def mark_as_done(item):
    item = urllib.parse.quote(item)
    requests.put(TODO_API_URL + "/api/items/" + item)
    return redirect(url_for("show_list"))


@app.route("/delete/<item>")
def delete_entry(item):
    item = urllib.parse.quote(item)
    requests.delete(TODO_API_URL + "/api/items/" + item)
    return redirect(url_for("show_list"))


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/exit")
def exit_app():
    global api_process
    if api_process:
        api_process.terminate()
    os._exit(0)


def run_todolist_api():
    try:
        todolist_api_2 = importlib.import_module("todolist_api_2")
    except ModuleNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    todolist_api_2.app.run(debug=True, use_reloader=False, port=5001)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    api_process = multiprocessing.Process(target=run_todolist_api)
    api_process.start()
    app.run(debug=True, use_reloader=False)
    api_process.join()

# import multiprocessing
# from flask import Flask, render_template, request, redirect, url_for, jsonify, session, current_app
# from flask_sqlalchemy import SQLAlchemy
# import requests
# import urllib.parse
# from flask_cors import CORS
# import importlib
# import sys

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todolist.db"
# app.config["SECRET_KEY"] = "mysecretkey"
# db = SQLAlchemy(app)
# CORS(app)

# TODO_API_URL = "http://127.0.0.1:5001"


# class Entry(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     what_to_do = db.Column(db.String(100))
#     due_date = db.Column(db.String(100))
#     status = db.Column(db.String(100))


# @app.route("/", methods=["GET", "POST"])
# def login():
#     error = None
#     if request.method == "POST":
#         if request.form["username"] != "student" or request.form["password"] != "student":
#             error = "Invalid credentials. Please try again."
#         else:
#             session["logged_in"] = True
#             return redirect(url_for("show_list"))
#     return render_template("login.html", error=error)


# @app.route("/todo", methods=["GET", "POST"])
# def show_list():
#     if not session.get("logged_in"):
#         return redirect(url_for("login"))

#     response = requests.get(TODO_API_URL + "/api/items")
#     items = response.json()
#     return render_template("index-2.html", items=items)


# @app.route("/add", methods=["POST"])
# def add_entry():
#     data = {"what_to_do": request.form["what_to_do"],
#             "due_date": request.form["due_date"],
#             "status": "open"}
#     response = requests.post(TODO_API_URL + "/api/items", json=data)
#     if response.status_code != 201:
#         return render_template("index-2.html", error="Failed to add item!")
#     return redirect(url_for("show_list"))


# @app.route("/mark/<item>")
# def mark_as_done(item):
#     item = urllib.parse.quote(item)
#     requests.put(TODO_API_URL + "/api/items/" + item)
#     return redirect(url_for("show_list"))


# @app.route("/delete/<item>")
# def delete_entry(item):
#     item = urllib.parse.quote(item)
#     requests.delete(TODO_API_URL + "/api/items/" + item)
#     return redirect(url_for("show_list"))


# @app.route("/logout")
# def logout():
#     session.pop("logged_in", None)
#     return redirect(url_for("login"))


# def run_todolist_api():
#     try:
#         todolist_api_2 = importlib.import_module("todolist_api_2")
#     except ModuleNotFoundError as e:
#         print(f"Error: {e}")
#         sys.exit(1)
#     todolist_api_2.app.run(debug=True, use_reloader=False, port=5001)


# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()

#     api_process = multiprocessing.Process(target=run_todolist_api)
#     api_process.start()
#     app.run(debug=True, use_reloader=False)
#     api_process.join()
