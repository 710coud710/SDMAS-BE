from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://dbpgf16628416:Z)Gdq8uU0J9gzFUPQXlhwfglV@serverless-europe-west2.sysp0000.db2.skysql.com:4007/sdmas_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    Member_id = db.Column(db.String(100))
    Password = db.Column(db.String(100))
    Club_id = db.Column(db.String(100))
    Full_name = db.Column(db.String(255))
    Birthday = db.Column(db.Date)
    Address = db.Column(db.String(255))
    Member_image = db.Column(db.String(255))
    Gender = db.Column(db.String(10))
    Join_date = db.Column(db.Date)
    Rank_id = db.Column(db.Integer)
    Received_rank = db.Column(db.String(100))
    Bio = db.Column(db.Text)
    Created = db.Column(db.DateTime)
    Updated = db.Column(db.DateTime)

@app.route('/members')
def get_members():
    members = Member.query.all()
    member_list = [{
        'id': member.id,
        'Member_id': member.Member_id,
        'Password': member.Password,
        'Club_id': member.Club_id,
        'Full_name': member.Full_name,
        'Birthday': member.Birthday,
        'Address': member.Address,
        'Member_image': member.Member_image,
        'Gender': member.Gender,
        'Join_date': member.Join_date,
        'Rank_id': member.Rank_id,
        'Received_rank': member.Received_rank,
        'Bio': member.Bio,
        'Created': member.Created,
        'Updated': member.Updated
    } for member in members]
    
    return jsonify(members=member_list)

if __name__ == "__main__":
    app.run(debug=True)
