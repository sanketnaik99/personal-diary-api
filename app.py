from flask import Flask, request, jsonify
import json
import os
import urllib.request
from flask_cors import CORS
import pymysql

# Constant For BASE URL
BASE_URL = "/api/v1/"
AUTH_CODE = "Sanketnaik@1999"

# Connect to MySQL database
db = pymysql.connect("remotemysql.com", "wHTjxfId7T", "6ETF8lfjGM", "wHTjxfId7T", port=3306, autocommit=True)
cursor = db.cursor()

# Initialize Flask App
app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.route(BASE_URL + 'create_db', methods=['POST'])
def create_db():
    data = request.form

    authentication = data['auth']

    if authentication == AUTH_CODE:
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS test_db;")
            cursor.execute('USE test_db')
            return jsonify({"result": "SUCCESS"})
        except:
            return jsonify({"result": "ERROR"})
    else:
        return jsonify({"result": "ERROR"})


@app.route(BASE_URL + 'add-user', methods=['POST'])
def add_user():
    data = request.form

    name = data['display_name']
    email = data['email']
    photoURL = data['photoURL']
    uid = data['uid']
    cursor.execute(
       "CREATE TABLE IF NOT EXISTS users (ID int NOT NULL AUTO_INCREMENT ,display_name VARCHAR(100), email VARCHAR(200), photoURL VARCHAR(1000), uid VARCHAR(100), PRIMARY KEY (ID));")

    cursor.execute(f'INSERT INTO users (display_name, email, photoURL, uid) VALUES ("{name}", "{email}", "{photoURL}", "{uid}");')

    return jsonify({"result": "SUCCESS"})


@app.route(BASE_URL + 'get_user_data', methods=['POST'])
def get_data():

    data = request.form
    email = data['email']

    cursor.execute(f"select * from users where email = '{email}'")
    data = cursor.fetchall()
    print(data)

    return jsonify(data)

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)