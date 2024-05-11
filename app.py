from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo
from pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Database setup
client = MongoClient('mongodb://localhost:27017/')
db = client.myAppDB
users = db.users

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if username is None or password is None:
        return jsonify({'message': 'Missing arguments'}), 400
    if users.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 400
    hash_pw = generate_password_hash(password)
    users.insert_one({'username': username, 'password': hash_pw, 'email': email})
    return jsonify({'message': 'User registered'}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True)