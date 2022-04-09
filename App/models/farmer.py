from App.database import db
from user import User

class Farmer(db.Model, User):
    contact = db.Column(db.String(7), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    profilePic = db.Column(db.String(150), nullable=True)
    profileHTML = db.Column(db.Text(), nullable=False)

    def __init__(self, username, password, firstName, lastName, contact, location):
        super().__init__(username, password, firstName, lastName)
        self.contact = contact
        self.location = location

    def __init__(self, username, password, firstName, lastName, contact, location, profilePic):
        super().__init__(username, password, firstName, lastName)
        self.contact = contact
        self.location = location
        self.profilePic = profilePic

    def setProfilePic(self, profilePic):
        self.profilePic = profilePic

    def toDict(self):
        dict = super().toDict()
        dict.contact = self.contact
        dict.location = self.location
        return dict
    
