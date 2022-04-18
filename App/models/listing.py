from App.database import db

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmerID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    # type = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(150), nullable=True)
    html = db.Column(db.Text(), nullable=True)

    def __init__(self, farmerID, name):
        self.farmerID = farmerID
        self.name = name
        self.html = ""

    def toDict(self):
        return {
            'id': self.id,
            'farmerID': self.farmerID,
            'name': self.name,
            'html': self.html
        }
