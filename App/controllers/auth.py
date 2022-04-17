import flask
import flask_login
# from flask_login import LoginManager, login_manager
from flask_jwt import JWT
from App.models import User


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return User.query.get(payload['identity'])

def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)


def logout_user():
    flask_login.logout_user()



def get_session():
    user = flask_login.current_user
    print(user.get_id())
    return user

def setup_jwt(app):
    return JWT(app, authenticate, identity)

def setup_flasklogin(app):
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    return login_manager