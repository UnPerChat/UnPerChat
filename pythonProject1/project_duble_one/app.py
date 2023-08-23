from flask import Flask, render_template, url_for, request, redirect
from kafka import KafkaConsumer
from kafka import KafkaProducer
import os
import time
import psycopg2
import bcrypt

import simplejson as json


app = Flask(__name__)
app.secret_key = "UnPerChat"

@app.route('/')
@app.route("/home")
def home():
    return render_template("home.html")


conn = psycopg2.connect(
    dbname="clients_data",
    user="postgres",
    password="kristi2005",
    host="localhost",
    port="5432"  # Default PostgreSQL port
)

cur = conn.cursor()
#
#
# @app.route("/register_check", methods=['GET', 'POST'])
# def register_check():
#     if request.method == 'POST':
#         req = request.form
#         req = dict(req)
#         print(req)
#
#         # No need to check for existing_user using client_id
#
#         insert_query = """
#             INSERT INTO clients_info (username, email, password, repeated_pass)
#             VALUES (%s, %s, %s, %s)
#         """
#         insert_data = (
#             req['username'],
#             req['email'],
#             req['password'],
#             req['repeated_pass']
#         )
#         cur.execute(insert_query, insert_data)
#         conn.commit()
#
#         return render_template("login.html")  # Or any other template
#
#     return render_template("register.html")
#         #     reg_query = """
#         #     INSERT INTO user_info (client_id, username, email, password)
#         #     VALUES (%s, %s, %s, %S)
#         #     """
#         #     reg_data = (req['client_id'], req['nickname'], req['email'], req['password'])
#         #     cur.execute(reg_query, reg_data)
#         #     conn.commit()
#         # else:
#         #     return render_template("error.html")
#
#

def user_exists(username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients_info WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    return user is not None

def email_already_logged(email):
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients_info WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user is not None

def login_correct_password(password, username):
    cur = conn.cursor()
    cur.execute("SELECT password FROM clients_info WHERE username = %s", (username,))
    stored_password = cur.fetchone()
    cur.close()

    if stored_password:
        if bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
            return True

    return False


@app.route('/register_check', methods=['GET', 'POST'])
def register_check():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Check if the user already exists
        if user_exists(username):
            return render_template("error.html")

        if email_already_logged(email):
            return render_template("error.html")

        cur = conn.cursor()
        cur.execute("INSERT INTO clients_info (username,email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        conn.commit()
        cur.close()

    return render_template('login.html')





@app.route('/register_check', methods=['GET', 'POST'])
def login_check():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']


            # Retrieve the hashed password from the database based on the username


        # Check if the user already exists
        if user_exists(username):
            return render_template("error.html")

        if email_already_logged(email):
            return render_template("error.html")

        cur = conn.cursor()
        cur.execute("INSERT INTO clients_info (username,email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
        conn.commit()
        cur.close()

    return render_template('login.html')














@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/error", methods=["GET", "POST"])
def error():
    return render_template("error.html")



if __name__ == '__main__':
    app.run(debug=True, threaded=True)

