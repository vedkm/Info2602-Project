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

def get_user_by_ID(id):
    return User.query.get(id).toDict()

def set_user_shopname(id, shopName):
    user = User.query.get(id)
    user.shopName = shopName
    db.session.add(user)
    db.session.commit()
    return user

def set_user_contact(id, contact):
    user = User.query.get(id)
    user.contact = contact
    db.session.add(user)
    db.session.commit()
    return user

def set_user_location(id, location):
    user = User.query.get(id)
    user.location = location
    db.session.add(user)
    db.session.commit()
    return user

def set_user_photo(id, photo):
    user = User.query.get(id)
    user.profilePic = photo
    db.session.add(user)
    db.session.commit()
    return user