from App.models import User
from App.database import db


def get_all_users():
    return User.query.all()

def create_user(username, password, shopName):
    newuser = User(username=username, password=password, shopName=shopName)
    db.session.add(newuser)
    db.session.commit()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toDict() for user in users]
    return users

def get_all_users():
    return User.query.all()