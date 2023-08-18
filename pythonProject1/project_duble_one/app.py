from flask import Flask, render_template, url_for, request, redirect
from kafka import KafkaConsumer
from kafka import KafkaProducer
import os
import time
import psycopg2
import simplejson as json


app = Flask(__name__)
app.secret_key = "UnPerChat"

@app.route('/')
@app.route("/home")
def home():
    return render_template("home.html")

conn = psycopg2.connect(
    host="localhost",
    port="5432",  # Default PostgreSQL port
    database="authentication",
    user="yourusername",
    password="yourpassword"
)

cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS user_info (
    id SERIAL PRIMARY KEY,
    nickname VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);
"""
cursor.execute(create_table_query)
conn.commit()

insert_query = """
INSERT INTO user_info (nickname, email, password)
VALUES (%s, %s, %s);
"""
user_data = ("user123", "user@example.com", "hashed_password")
cursor.execute(insert_query, user_data)
conn.commit()

cursor.close()
conn.close()


@app.route("/register_check", methods=['GET', 'POST'])
def register_check():
    return render_template("register.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process the form data, validate, and save to the database
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        password = request.form.get('password')

        # Perform validation and database operations here

        return "Registration successful!"

    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the login form data, validate, and authenticate the user
        email = request.form.get('email')
        password = request.form.get('password')

        # Perform authentication and validation here
        # If authentication succeeds, redirect the user to a dashboard or other page

        return "Login successful!"

    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True, threaded=True)