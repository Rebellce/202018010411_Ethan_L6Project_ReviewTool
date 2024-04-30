import base64
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
            session['id'] = code
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
            session['id'] = user['id']
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
    session.pop('id', None)
    session.pop('user', None)
    session.pop('firstName', None)
    session.pop('lastName', None)
    session.pop('avatar', None)
    return jsonify({'message': 'Logged out successfully!'}), 200


@app.route('/upload/new/png', methods=['POST'])
def uploadPNG():
    if 'user' in session:
        try:
            json = request.get_json()
            userId = session['id']
            recordName = json['name']
            recordType = 'File'
            data = (userId, recordName, recordType)
            print(data)
            recordId = db.addRecord(data)
            if recordId is None:
                return jsonify({'message': 'Error uploading file!'}), 500
            image = json['image']
            imageBytes = base64.b64decode(image)
            _path = f"static/userUpload/{userId}/"
            if not os.path.exists(_path):
                os.makedirs(_path)
            _path = f"{_path}{recordId}.png"
            with open(_path, "wb") as file:
                file.write(imageBytes)
            fileRecordId = db.addFileRecord((recordId, _path))
            if fileRecordId is None:
                return jsonify({'message': 'Error uploading file!'}), 500
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error uploading file!'}), 500

        return jsonify({'message': recordId}), 200
    else:
        return jsonify({'message': 'User not logged in!'}), 400


@app.route('/upload/new/ocr', methods=['POST'])
def uploadOCR():
    if 'user' in session:
        try:
            json = request.get_json()
            userId = session['id']
            recordName = json['name']
            recordType = 'OCR'
            data = (userId, recordName, recordType)
            print(data)
            recordId = db.addRecord(data)
            if recordId is None:
                return jsonify({'message': 'Error uploading file!'}), 500
            text = json['text']
            textRecordId = db.addTextRecord((recordId, text))
            if textRecordId is None:
                return jsonify({'message': 'Error uploading file!'}), 500
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error uploading file!'}), 500

        return jsonify({'message': recordId}), 200
    else:
        return jsonify({'message': 'User not logged in!'}), 400


@app.route('/upload/new/ai', methods=['POST'])
def uploadAI():
    if 'user' in session:
        try:
            json = request.get_json()
            userId = session['id']
            recordName = json['name']
            recordType = 'AI'
            data = (userId, recordName, recordType)
            print(data)
            recordId = db.addRecord(data)
            if recordId is None:
                return jsonify({'message': 'Error uploading file!'}), 500
            dicts = json['dicts']
            for dic in dicts:
                textRecordId = db.addTextRecord((recordId, dic['content']))
                if textRecordId is None:
                    return jsonify({'message': 'Error uploading file!'}), 500
                detectionId = db.addDetection((textRecordId, dic['proportion']))
                if detectionId is None:
                    return jsonify({'message': 'Error uploading file!'}), 500
        except Exception as e:
            print(e)
            return jsonify({'message': 'Error uploading file!'}), 500

        return jsonify({'message': recordId}), 200
    else:
        return jsonify({'message': 'User not logged in!'}), 400


@app.route('/load/records', methods=['GET'])
def loadRecords():
    if 'user' in session:
        userId = session['id']
        records = db.getRecords(userId)
        if records is not None:
            for record in records:
                record['timestamp'] = record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            return jsonify({'records': records}), 200
        else:
            return jsonify({'message': 'No records found!'}), 400
    else:
        return jsonify({'message': 'User not logged in!'}), 400


@app.route('/delete/record', methods=['POST'])
def deleteRecord():
    if 'user' in session:
        userId = session['id']
        recordId = request.json.get('recordId')

        result = db.getRecord(recordId)
        if not result:
            return jsonify({'message': 'Record not found!'}), 400
        _type = result[0]['type']
        if _type == 'File':
            fileRecord = db.deleteFileRecord(recordId)
            if not fileRecord:
                return jsonify({'message': 'Error deleting record!'}), 500
            path = f"static/userUpload/{userId}/{recordId}.png"
            if os.path.exists(path):
                os.remove(path)
        else:
            textID = db.getTextRecord(recordId)
            if textID:
                textID = textID[0]['id']
                if _type == 'Ai':
                    db.deleteDetection(textID)
                db.deleteTextRecord(recordId)
        db.deleteRecord(recordId)
        return jsonify({'message': 'Record deleted successfully!'}), 200
    else:
        return jsonify({'message': 'User not logged in!'}), 400


@app.route('/load/file/<int:recordId>', methods=['GET'])
def loadFileRecord(recordId):
    if 'user' in session:
        result = db.getFileRecord(recordId)
        if not result:
            return jsonify({'message': 'Record not found!'}), 400
        path = result[0]['path']
        with open(path, "rb") as image_file:
            img = base64.b64encode(image_file.read()).decode('utf-8')
        return jsonify({'image': img}), 200


@app.route('/load/ocr/<int:recordId>', methods=['GET'])
def loadOCRRecord(recordId):
    if 'user' in session:
        result = db.getTextRecord(recordId)
        if not result:
            return jsonify({'message': 'Record not found!'}), 400
        text = result[0]['content']
        return jsonify({'text': text}), 200


@app.route('/load/ai/<int:recordId>', methods=['GET'])
def loadAIRecord(recordId):
    if 'user' in session:
        lst = []
        results = db.getTextRecord(recordId)
        if not results:
            return jsonify({'message': 'Record not found!'}), 400
        for result in results:
            textId = result['id']
            detection = db.getDetection(textId)
            if detection:
                detection = detection[0]
                lst.append({'content': result['content'], 'proportion': detection['proportion']})
        return jsonify({'data': lst}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
