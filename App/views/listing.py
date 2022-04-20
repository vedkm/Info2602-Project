import json
import os
from flask import Blueprint, flash, redirect, render_template, request
from flask_login import login_required
from App.controllers.listing import *
from App.controllers.user import get_user_by_ID
from App.models import db, User, Listing, listing

from werkzeug.utils import secure_filename

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

# use this route to add a new listing
# an "Add Listing" form should call this route
@listing_views.route("/listing", methods=["POST", "GET"])
def add_listing():
    if (request.method == "POST"):
        data = request.form
        farmerID = request.args.get('farmerID')
        listing = addListing(farmerID=farmerID, name=data['name'], html=data['html'])
        # flash("Listing Added with ID: " + listing.id)
        return redirect("/listing/"+str(listing['id']))
    if (request.method == "GET"):
        return render_template("createlisting.html")

# use this route to get a listing by ID and render it to the page
@listing_views.route("/listing/<id>", methods=["GET", "DELETE"])
def get_listing(id):
    if (request.method == "DELETE"):
        deleteListing(id=id)
        return redirect("profile")

    listing = getListingByID(id)
    farmer = get_user_by_ID(listing['farmerID'])
    if (not listing):
        flash("No Such Listing.", "error")
        # return redirect("/")
        return render_template("index.html")
    return render_template("listing.html", listing=listing, farmer=farmer)

@listing_views.route('/savelistinghtml', methods=['PUT'])
def save():

    if (request.files and request.files['image_param']):
        image = request.files['image_param']
        filename = secure_filename(image.filename)
        
        path = os.path.realpath( os.path.realpath("App/static/uploaded") + "/" + filename)
        print(path)
        status = image.save(path, image.content_length)
        return {
            "link": "/static/uploaded/"+filename
        }

    if ('html' in request.form):
        html = request.form['html']
        id = request.form['id']
        farmerID = request.form['farmerID']
        name = request.form['name']
        print(id)
        print(html)
        listing = Listing.query.get(id)
        if (not listing):
            db.session.add(Listing(farmerID, html, name))
            db.session.commit()
            print("Listing Created")
            return "Listing Created"
        return setListingHTML(id=id, html=html)

    return request.form

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