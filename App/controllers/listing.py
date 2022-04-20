from flask_login import current_user
from App.models import Listing
from App.database import db

def addListing(farmerID, name, html):
    try:
        listing = Listing(farmerID=farmerID, name=name, html=html)
        db.session.add(listing)
        db.session.commit()
    except:
        return None
    return listing.toDict()

def getAllListings():
    listings = Listing.query.all()
    listings = [list.toDict() for list in listings]
    return listings

def getListingByID(id):
    listing = Listing.query.get(id)
    if (not listing): return None
    return listing.toDict()

def getListingsByFarmer(id):
    listings = Listing.query.filter_by(farmerID=id)
    if (not listings): return None
    listings = [list.toDict() for list in listings]
    return listings

def deleteListing(id):
    listing = Listing.query.get(id)
    if (not listing): return None
    db.session.delete(listing)
    return db.session.commit()

def setListingHTML(id, html):
    listing = Listing.query.get(id)
    listing.html = html
    db.session.add(listing)
    db.session.commit()
    return listing.toDict()