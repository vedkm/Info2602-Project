import json
from flask import Blueprint, flash, redirect, render_template, request
from flask_login import login_required
from App.models import db, User, Listing

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

# use this route to add a new listing
# an "Add Listing" form should call this route
@listing_views.route("/listing", methods=["POST"])
def add_listing():
    if (request.method == "POST"):
        data = request.form
        listing = Listing(farmerID=data['farmerID'], name=data['name'])
        db.session.add(listing)
        db.session.commit()
        # flash("Listing Added with ID: " + listing.id)
        return redirect("/farmers")

# use this route to get a listing by ID and render it to the page
@listing_views.route("/listing/<id>", methods=["GET"])
def get_listing(id):
    listing = Listing.query.get(id)
    if (listing != None): listing = listing.toDict()
    return render_template("listing.html", listing=listing)

@listing_views.route('/listings')
def get_listings():
    id = request.args.get('id')
    listings = []
    if (id):
        listings = Listing.query.get(id)
        if (not listings):
            listings = []
        else:
            listings = listings.toDict()
    else:
        listings = Listing.query.all()
        listings = [list.toDict() for list in listings]
    return json.dumps(listings)