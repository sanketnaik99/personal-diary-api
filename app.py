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
db = pymysql.connect("remotemysql.com", "a0EjWgNg3d", "xgrm2qldV8", "a0EjWgNg3d", port=3306, autocommit=True)
cursor = db.cursor()

# Initialize Flask App
app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

#
# CREATE DATABASE
#
@app.route(BASE_URL + 'create_db', methods=['POST'])
def create_db():
    data = request.form

    authentication = data['auth']

    if authentication == AUTH_CODE:
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS personal_diary;")
            cursor.execute('USE personal_diary')
            return jsonify({"result": "SUCCESS"})
        except:
            return jsonify({"result": "ERROR"})
    else:
        return jsonify({"result": "ERROR"})


#
# START OF USER ACTIONS
#
app.route(BASE_URL + 'add-user', methods=['POST'])
def add_user():
    data = request.form

    name = data['display_name']
    email = data['email']
    photoURL = data['photoURL']
    uid = data['uid']
    try:
        cursor.execute(
       "CREATE TABLE IF NOT EXISTS users (ID int NOT NULL AUTO_INCREMENT ,display_name VARCHAR(100), email VARCHAR(200), photoURL VARCHAR(1000), uid VARCHAR(100), PRIMARY KEY (ID));")

        cursor.execute(f'INSERT INTO users (display_name, email, photoURL, uid) VALUES ("{name}", "{email}", "{photoURL}", "{uid}");');
        return jsonify({"result": "SUCCESS"})

    except:
        return jsonify({"result": "ERROR"})


@app.route(BASE_URL + 'get-user-data', methods=['POST'])
def get_user_data():

    data = request.form
    email = data['email']

    try:
        cursor.execute(f"select * from users where `email` = \"{email}\"")
        data = cursor.fetchone()
        return jsonify({"result": "SUCCESS", "data": data})
    except:
        return jsonify({"result": "ERROR"})

#
# END OF USER ACTIONS
#

#
# START OF DIARY ACTIONS
#
@app.route(BASE_URL + 'add-entry', methods=['POST'])
def add_entry():

    formData = request.form
    uid = formData["uid"]
    id = formData["id"]
    data = formData["data"]
    month = formData["month"]
    year = formData["year"]
    date = formData["date"]
    day = formData["day"]

    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {uid}_diary (UID int NOT NULL AUTO_INCREMENT, id VARCHAR(20), date VARCHAR(10), month VARCHAR(20), year VARCHAR(10), day VARCHAR(10), data VARCHAR(2000), PRIMARY KEY (UID));")
        cursor.execute(f"insert into {uid}_diary (id, date, month, year, day, data) VALUES (\"{id}\", \"{date}\", \"{month}\", \"{year}\", \"{day}\", \"{data}\");")

        return jsonify({"result": "SUCCESS"})
    except:
        return jsonify({"result": "ERROR"})


@app.route(BASE_URL + 'get-data', methods=['POST'])
def get_diary_data():

    data = request.form
    uid = data['uid']

    try:
        cursor.execute(f"select * from {uid}_diary ORDER BY id DESC;")
        result = cursor.fetchall()
        return jsonify({"result": "SUCCESS", "data": result})
    except:
        return jsonify({"result": "ERROR"})


@app.route(BASE_URL + 'update-entry', methods=['POST'])
def update_entry():

    formData = request.form
    uid = formData['uid']
    data = formData['data']
    id = formData['id']

    try:
        cursor.execute(f'update {uid}_diary SET  `data` = "{data}" where id = "{id}";')
        return jsonify({"result": "SUCCESS"})
    except:
        return jsonify({"result": "ERROR"})

#
# END OF DIARY ACTIONS
#

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
