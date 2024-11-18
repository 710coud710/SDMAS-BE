import datetime
import jwt
from flask import Blueprint, request, jsonify
from app.config import Config
import mariadb
import sys

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Hết hạn sau 1 giờ
        'iat': datetime.datetime.utcnow()  # Thời điểm tạo
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    member_id = data.get('member_id')
    password = data.get('password')

    if not member_id or not password:
        return jsonify(message="Member ID and password are required."), 400

    conn = mariadb.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )
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
