from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    shopName = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(7), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    profilePic = db.Column(db.String(150), nullable=True)
    profileHTML = db.Column(db.Text(), nullable=True)

    def __init__(self, username, password, shopName):
        self.username = username
        self.set_password(password)
        self.shopName = shopName
        # self.firstName = firstName
        # self.lastName = lastName

    def toDict(self):
        return{
            'id': self.id,
            'username': self.username,
            'shopName': self.shopName
            # 'firstName': self.firstName,
            # 'lastName': self.lastName
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

