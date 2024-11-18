from app import db

class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    club_id = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(255), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    member_image = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    join_date = db.Column(db.Date, nullable=True)
    rank_id = db.Column(db.String(255), nullable=True)
    received_rank = db.Column(db.DateTime, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f'<Member {self.full_name}>'

    def serialize(self):
        return {
            "id": self.id,
            "member_id": self.member_id,
            "password": self.password,
            "club_id": self.club_id,
            "full_name": self.full_name,
            "birthday": self.birthday.strftime('%Y-%m-%d') if self.birthday else None,
            "address": self.address,
            "member_image": self.member_image,
            "gender": self.gender,
            "join_date": self.join_date.strftime('%Y-%m-%d') if self.join_date else None,
            "rank_id": self.rank_id,
            "received_rank": self.received_rank.strftime('%Y-%m-%d %H:%M:%S') if self.received_rank else None,
            "bio": self.bio,
            "created": self.created.strftime('%Y-%m-%d %H:%M:%S') if self.created else None,
            "updated": self.updated.strftime('%Y-%m-%d %H:%M:%S') if self.updated else None,
        }
