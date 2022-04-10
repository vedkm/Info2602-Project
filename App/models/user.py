from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # firstName = db.Column(db.String(50), nullable=False)
    # lastName = db.Column(db.String(50), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        # self.firstName = firstName
        # self.lastName = lastName

    def toDict(self):
        return{
            'id': self.id,
            'username': self.username,
            # 'firstName': self.firstName,
            # 'lastName': self.lastName
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

