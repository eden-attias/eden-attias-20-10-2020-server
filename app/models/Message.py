from datetime import datetime

from app import db


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)  # message id
    sender = db.Column(db.String(collation='utf8_general_ci', length=32))
    receiver = db.Column(db.String(collation='utf8_general_ci', length=32))
    subject = db.Column(db.String(collation='utf8_general_ci', length=32))
    message = db.Column(db.String(collation='utf8_general_ci', length=1024))
    deleted_by_sender = db.Column(db.Boolean())
    deleted_by_receiver = db.Column(db.Boolean())
    creation_date = db.Column(db.DateTime())

    def __init__(self, sender, receiver, subject, message):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.message = message
        self.creation_date = datetime.now()
        self.deleted_by_receiver = False
        self.deleted_by_sender = False
