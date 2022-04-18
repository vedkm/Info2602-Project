from App.models import Listing
from App.database import db

def addListing(farmerID, name):
    try:
        listing = Listing(farmerID=farmerID, name=name)
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

def setListingHTML(id, html):
    listing = Listing.query.get(id)
    listing.html = html
    try:
        db.session.add(listing)
    except:
        return None
    db.session.commit()
    return listing.toDict()