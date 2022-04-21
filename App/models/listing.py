from App.database import db

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmerID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    html = db.Column(db.Text(), nullable=True)

    def __init__(self, farmerID, name, html):
        self.farmerID = farmerID
        self.name = name
        self.html = html

    def toDict(self):
        return {
            'id': self.id,
            'farmerID': self.farmerID,
            'name': self.name,
            'html': self.html
        }
