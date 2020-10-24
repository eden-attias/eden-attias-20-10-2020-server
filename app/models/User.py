from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)  # user id
    user_name = db.Column(db.String(collation='utf8_general_ci', length=32), unique=True)
    password_hash = db.Column(db.String(collation='utf8_general_ci', length=128))  # Password hash of agent
    name = db.Column(db.String(collation='utf8_general_ci', length=64))
    email = db.Column(db.String(collation='utf8_general_ci', length=64), unique=True)

    def __init__(self, user_name, password_hash, name, email):
        self.user_name = user_name
        self.name = name
        self.password_hash = password_hash
        self.email = email
