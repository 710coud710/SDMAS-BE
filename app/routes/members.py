from flask import Blueprint, jsonify
import mariadb
from app.config import Config

members_bp = Blueprint('members', __name__)

@members_bp.route('/members', methods=['GET'])
def get_members():
    conn = mariadb.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )
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
