import os

from flask import Flask, request, jsonify, session
import DBManager as db
import hashlib

app = Flask(__name__)
# app.secret_key = os.urandom(24)
app.secret_key = 'super secret key'


@app.route('/test', methods=['POST'])
def loginTest():
    username = request.json.get('username')
    password = request.json.get('password')
    print(username, password)

    if username == 'test' and password == '123456':
        session['user'] = username  # 在会话中存储用户
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401


@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    firstName = request.json.get('firstName')
    lastName = request.json.get('lastName')
    avatar = r'userUpload\default\avatar.png'
    print("Register..")
    print(email, password, firstName, lastName)
    if db.getUserByEmail(email):
        return jsonify({'message': 'User already exists!'}), 400
    else:
        code = db.addUser((email, firstName, lastName, password, avatar))
        if code is None:
            return jsonify({'message': 'User creation failed!'}), 500
        else:
            session['user'] = email
            session['firstName'] = firstName
            session['lastName'] = lastName
            session['avatar'] = avatar
            return jsonify({'message': 'User created successfully!'}), 200


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    print("Login..")
    print(email, password)
    user = db.getUserByEmail(email)
    if user:
        if user['password'] == password:
            session['user'] = email
            session['firstName'] = user['first_name']
            session['lastName'] = user['last_name']
            session['avatar'] = user['avatar']
            return jsonify({'message': 'Login successful!'}), 200
        else:
            return jsonify({'message': 'Invalid credentials!'}), 400


@app.route('/getUser', methods=['GET'])
def getUser():
    if 'user' in session:
        return jsonify(
            {'email': session['user'], 'firstName': session['firstName'], 'lastName': session['lastName']}), 200
    else:
        return jsonify({'message': 'User not logged in!'}), 400


@app.route('/logout', methods=['GET'])
def logout():
    print("Logging out...")
    session.pop('user', None)
    session.pop('firstName', None)
    session.pop('lastName', None)
    session.pop('avatar', None)
    return jsonify({'message': 'Logged out successfully!'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
