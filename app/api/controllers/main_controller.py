from datetime import timedelta

from flask_jwt_extended import create_access_token
from sqlalchemy import or_
from werkzeug.routing import ValidationError
from passlib.hash import pbkdf2_sha256

from app import User, Message, db


def login(body):
    user_name = body['user_name']
    password = body['password']

    if not user_name:
        raise ValidationError("User name missing", 401)
    if not password:
        raise ValidationError("Password is missing", 401)

    current_user = User.query.filter(User.user_name == user_name).first()

    if current_user is None:
        raise ValidationError('User or password are incorrect')

    if not pbkdf2_sha256.verify(password, current_user.password_hash):
        raise ValueError('Password is incorrect')

    response = {"token": create_access_token(identity=user_name),
                "name": current_user.name,
                "id": current_user.id,
                "user_name": current_user.user_name,
                "email": current_user.email}

    return response


def register(body):
    user_name = body['user_name']
    password = body['password']
    name = body['name']
    email = body['email']

    user = User.query.filter(User.email == email).first()

    if user is not None:
        raise ValidationError("Mail already exsists", 401)

    if not user_name:
        raise ValidationError("User name missing", 401)

    if not password:
        raise ValidationError("Password is missing", 401)

    if not name:
        raise ValidationError("Name is missing", 401)

    if not email:
        raise ValidationError("Email is missing", 401)

    new_user = User(name=name, user_name=user_name, password_hash=pbkdf2_sha256.hash(password), email=email)
    db.session.add(new_user)
    db.session.commit()
    db.session.flush()

    return {"status": True}


def get_messages_by_user_id(args):
    user_id = args.get('user_id')

    if user_id is None:
        raise ValidationError("Invalid User id", 401)

    current_user = User.query.filter(User.id == user_id).first()

    if current_user is None:
        raise ValidationError("User is not exists", 401)

    messages = Message.query.filter(
        or_(Message.receiver == current_user.email, Message.sender == current_user.email)).all()

    messages_response = []

    for m in messages:

        if m.deleted_by_receiver == False and m.receiver == current_user.email \
                or m.deleted_by_sender == False and m.sender == current_user.email:
            message = {'subject': m.subject,
                       'id': m.id,
                       'sender': m.sender,
                       'receiver': m.receiver,
                       'message': m.message,
                       'creation_date': m.creation_date
                       }

            messages_response.append(message)

    return {'messages': messages_response}


def add_message(body):
    subject = body['subject']
    sender = body['sender']
    receiver_name = body['receiver']
    message = body['message']

    if subject is None:
        raise ValidationError("Subject is missing", 401)

    if sender is None:
        raise ValidationError("Sender is missing", 401)

    if receiver_name is None:
        raise ValidationError("Receiver is missing", 401)

    if message is None:
        raise ValidationError("Message is missing", 401)

    current_user = User.query.filter(User.email == sender).first()

    if current_user is None:
        raise ValidationError("Invalid sender", 401)

    new_message = Message(sender=sender, receiver=receiver_name, subject=subject, message=message)

    db.session.add(new_message)
    db.session.commit()
    db.session.flush()

    return {'status': True}


def delete_messages_by_id(body):
    messages_ids = body['messages_ids']
    user_id = body['user_id']

    if messages_ids is None:
        raise ValidationError("Invalid request", 401)

    if len(messages_ids) == 0:
        raise ValidationError("No messages was selected", 401)

    current_user = User.query.filter(User.id == user_id).first()

    for message_id in messages_ids:

        current_message = Message.query.filter(Message.id == message_id).first()

        if current_message is not None:

            if current_message.receiver == current_user.email:
                current_message.deleted_by_receiver = True
            else:
                current_message.deleted_by_sender = True

            if current_message.deleted_by_receiver and current_message.deleted_by_sender:
                db.session.delete(current_message)
            db.session.commit()
            db.session.flush()

    return {'status': True}
