from App.database import db, farmer

class Listing(db.Model):
    id = db.Column(db.Integer, nullable=False)
    farmerID = db.Column(db.Integer, db.ForeignKey(farmer.id), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    photo = db.Column(db.String(150), nullable=False)
    listingHTML = db.Column(db.Text(), nullable=False)

    def __init__(self, farmerID, title, type, photo):
        self.farmerID = farmerID
        self.title = title
        self.type = type
        self.photo = photo

    def toDict(self, farmerID, title, type, photo):
        return {
            'id': self.id,
            'farmerID': self.farmerID,
            'title': self.title,
            'type': self.type,
            'photo': self.photo
        }
