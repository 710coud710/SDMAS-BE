# app.py
import datetime
import bcrypt
from flask import Flask, jsonify, request
import json
import jwt
import mariadb
import sys
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Kết nối với SkySQL
def get_db_connection():
    try:
        conn = mariadb.connect(
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME'], 
            ssl_verify_cert=app.config['DB_SSL_VERIFY']
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

# Route kiểm tra kết nối cơ sở dữ liệu
@app.route('/db-test')
def db_test():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Thực hiện một truy vấn cơ bản
    cursor.execute("SELECT * FROM members")
    row = cursor.fetchone()
    
    conn.close()
    
    return jsonify(message=row[0])
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Hết hạn sau 1 giờ
        'iat': datetime.datetime.utcnow()  # Thời điểm tạo
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token
def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def hello():
    return jsonify(message="Hello, SkySQL!")
@app.route('/api/members')
def get_members():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Truy vấn lấy tất cả dữ liệu từ bảng members
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()  # Lấy tất cả dòng dữ liệu

    # Tạo danh sách các dict chứa dữ liệu của mỗi member
    member_list = []
    for member in members:
        member_list.append({
            'id': member[0],
            'Member_id': member[1],
            'Password': member[2],
            'Club_id': member[3],
            'Full_name': member[4],
            'Birthday': member[5],
            'Address': member[6],
            'Member_image': member[7],
            'Gender': member[8],
            'Join_date': member[9],
            'Rank_id': member[10],
            'Received_rank': member[11],
            'Bio': member[12],
            'Created': member[13],
            'Updated': member[14]
        })

    conn.close()
    return jsonify(members=member_list)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    member_id = data.get('member_id')
    password = data.get('password')

    if not member_id or not password:
        return jsonify(message="Member ID and password are required."), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, Password FROM members WHERE Member_id = ?",
            (member_id,)
        )
        result = cursor.fetchone()

        if result:
            user_id = result[0]
            
            token = generate_token(user_id)
            return jsonify(
                message="Login successful.",
                token=token
            )
        else:
                return jsonify(message="Invalid password."), 401

    finally:
        conn.close()

@app.route('/api/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify(message="Token is missing."), 401

    token = token.replace("Bearer ", "")

    user_id = decode_token(token)
    if not user_id:
        return jsonify(message="Invalid or expired token."), 401

    return jsonify(message="Protected route accessed.", user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)
