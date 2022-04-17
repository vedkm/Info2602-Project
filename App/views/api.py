# from crypt import methods
import json
import os
from flask import Blueprint, redirect, render_template, request, send_from_directory, session
from flask_login import login_required
from sqlalchemy import JSON
from werkzeug.utils import secure_filename
from flask_jwt import jwt_required
from App.controllers.auth import authenticate, get_session, login_user

from App.models import user
from ..models import db, User, Listing

import App

api_views = Blueprint('api_views', __name__, template_folder='../templates')

@api_views.route('/', methods=['GET'])
def get_api_docs():
    return render_template('index.html')

@api_views.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() 
    username = data['username']
    password = data['password']
    shopName = data['shopName']
    db.session.add(User(username, password, shopName))
    db.session.commit()
    return "Added User"

@api_views.route("/login", methods=["POST", "GET"])
def loginAction():
    if (request.method == "POST"):
        data = request.get_json()
        user = authenticate(data['username'], data['password'])
        if (user):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            status = login_user(user, remember=True)
            if (status == True):
                session = get_session()
                # return session.toDict()
                return render_template("login.html")
    
    return render_template("login.html")

@api_views.route('/save', methods=['PUT'])
def update_froala_text():
    html = request.form['content']
    id = request.form['id']
    userID = request.form['userID']
    print(id)
    print(html)
    listing = Listing.query.get(id)
    if (listing == None):
        db.session.add(Listing(userID, html))
        db.session.commit()
        print("Listing Created")
        return "Listing Created"
    
    listing.html = html
    db.session.add(listing)
    db.session.commit()
    return html

# can return an array of listings if we end up doing multiple editors in 1 page
@api_views.route('/farmers')
def get_editor():
    listing = Listing.query.get(1)
    if (listing == None): return render_template("editor.html")
    # print(listing.toDict())
    return render_template("editor.html", listingHTML=listing.html)

UPLOAD_FOLDER = "C:/Users/User/OneDrive - The University of the West Indies, St. Augustine/year 2/INFO 2602/Info2602 Project/App/images"
# App.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@api_views.route('/upload_froala_image', methods=['POST'])
def post_froala_image():
    image = request.files['image_param']
    # path = os.path.join(UPLOAD_FOLDER, secure_filename(image.filename))

    # may not return unique
    filename = secure_filename(image.filename)

    path = UPLOAD_FOLDER + "/" + filename
    image.save(path, image.content_length)
    print(path)
    return {
        "link": "images/"+filename
    }

# allows the text editor to fetch the saved image from server,
# note that this is not private
@api_views.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@api_views.route('/listings')
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

