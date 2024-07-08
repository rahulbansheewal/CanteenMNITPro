from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import jwt
import datetime

app = Flask(__name__)
CORS(app)

SECRET_KEY = 'your_secret_key'

@app.route('/api/status', methods=['GET'])
def status():
    return "Server is running"

@app.route('/api/token', methods=['GET'])
def get_token():
    token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, SECRET_KEY, algorithm='HS256')
    return jsonify({'token': token})

@app.route('/api/purchase', methods=['POST'])
def purchase():
    token = request.headers.get('Authorization')
    if not token or not verify_token(token):
        return 'Unauthorized', 401
    
    data = request.json
    if not validate_schema(data):
        return 'Invalid data schema', 400
    
    try:
        insert_data(data)
        return 'POST request received', 200
    except Exception as e:
        return str(e), 500

def verify_token(token):
    try:
        jwt.decode(token.split(' ')[1], SECRET_KEY, algorithms=['HS256'])
        return True
    except jwt.InvalidTokenError:
        return False

def validate_schema(data):
    required_fields = ['name', 'date', 'time', 'item', 'quantity', 'payment', 'role', 'location']
    return all(field in data for field in required_fields)

def insert_data(data):
    conn = sqlite3.connect('canteen.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO canteen_purchases (name, date, time, item, quantity, payment, role, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['date'], data['time'], data['item'], data['quantity'], data['payment'], data['role'], data['location']))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(port=8080)
