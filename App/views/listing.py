import json
from flask import Blueprint, flash, redirect, render_template, request
from flask_login import login_required
from App.controllers.listing import *
from App.models import db, User, Listing, listing

from werkzeug.utils import secure_filename

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')

# use this route to add a new listing
# an "Add Listing" form should call this route
@listing_views.route("/listing", methods=["POST"])
def add_listing():
    if (request.method == "POST"):
        data = request.form
        listing = addListing(farmerID=data['farmerID'], name=data['name'])
        # flash("Listing Added with ID: " + listing.id)
        return redirect("/listing/"+str(listing['id']))

# use this route to get a listing by ID and render it to the page
@listing_views.route("/listing/<id>", methods=["GET"])
def get_listing(id):
    listing = getListingByID(id)
    if (not listing):
        flash("No Such Listing.", "error")
        return redirect("/")
    return render_template("listing.html", listing=listing)

@listing_views.route('/savelistinghtml', methods=['PUT'])
def save():

    if (request.files and request.files['image_param']):
        image = request.files['image_param']
        filename = secure_filename(image.filename)
        # change to relative path
        UPLOAD_FOLDER = "C:/Users/User/OneDrive - The University of the West Indies, St. Augustine/year 2/INFO 2602/Info2602 Project/App/images"
        path = UPLOAD_FOLDER + "/" + filename
        image.save(path, image.content_length)
        print(path)
        return {
            "link": "http://localhost:8080/images/"+filename
        }

    if (request.form['html']):
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
    
    listing.html = html
    db.session.add(listing)
    db.session.commit()
    return html

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