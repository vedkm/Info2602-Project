from App.database import db

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    farmerID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # title = db.Column(db.String(20), nullable=False)
    # type = db.Column(db.String(20), nullable=False)
    # photo = db.Column(db.String(150), nullable=False)
    html = db.Column(db.Text(), nullable=False)

    def __init__(self, farmerID, html):
        self.farmerID = farmerID
        self.html = html

    def toDict(self):
        return {
            'id': self.id,
            'farmerID': self.farmerID,
            'listingHTML': self.html
        }
