# from crypt import methods
import json
import os
from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import login_required, current_user
from sqlalchemy import JSON, false
from werkzeug.utils import secure_filename
from flask_jwt import jwt_required
from App.controllers.auth import authenticate, get_session, login_user, logout_user
from App.controllers.listing import getAllListings, getListingsByFarmer
from App.controllers.user import get_user_by_ID, set_user_contact, set_user_location, set_user_photo, set_user_shopname

from App.models import user
from ..models import db, User, Listing

import App

api_views = Blueprint('api_views', __name__, template_folder='../templates')

@api_views.route('/', methods=['GET'])
def get_api_docs():
    listings = getAllListings()
    if (listings == None): return render_template("profile.html")
    data = []
    for listing in listings:
        data.append({
            'listing': listing,
            'farmer': get_user_by_ID(listing['farmerID'])
        })
    return render_template("index.html", data=data)

@api_views.route('/signup', methods=['POST', 'GET'])
def signup():
    if (request.method == "POST"):
        data = request.form
        username = data['username']
        password = data['password']
        shopName = data['shopName']
        contact = data['contact']
        location = data['location']

        if ('image' in request.files and request.files['image'].filename):
            image = request.files['image']
            filename = secure_filename(image.filename)
            path = os.path.realpath( os.path.realpath("App/static/uploaded") + "/" + filename)
            status = image.save(path, image.content_length)
            db.session.add(User(username, password, shopName, contact, location, "static/uploaded/"+filename))
            db.session.commit()
            return redirect('/login')

        db.session.add(User(username, password, shopName, contact, location))
        db.session.commit()
        return redirect('/login')
        # return render_template('profile.html')
    if (request.method == "GET"):
        return render_template('signup.html')

@api_views.route("/login", methods=["POST", "GET"])
def loginAction():
    if (request.method == "POST"):
        data = request.form
        user = authenticate(data['username'], data['password'])
        if (user):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            status = login_user(user, remember=True)
            if (status == True):
                #  session = get_session()
                #  return session.toDict()
                #  return redirect("/profile")
                return redirect("/profile")
               

    flash("Invalid username or password. Would you like to signup?", "error")
    error = "Invalid username or password. Would you like to signup?"
    return render_template("login.html", error=error)

@api_views.route("/logout", methods=["GET"])
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect("/login")
    # return render_template("login.html")

@api_views.route('/save', methods=['PUT'])
def update_froala_text():
    html = request.form['content']
    id = request.form['id']
    userID = request.form['userID']
    name = request.form['name']
    print(id)
    print(html)
    listing = Listing.query.get(id)
    if (listing == None):
        db.session.add(Listing(userID, html, name))
        db.session.commit()
        print("Listing Created")
        return "Listing Created"
    
    listing.html = html
    db.session.add(listing)
    db.session.commit()
    return html


@api_views.route('/profile')
def get_profile():

    profile = None
    if (not request.args.get('id')):
        if (current_user.is_authenticated):
            profile = current_user.toDict()
    elif (request.args.get('id')):
        profile = get_user_by_ID(request.args.get('id'))
    else:
        profile = get_user_by_ID(1)

    listings = getListingsByFarmer(profile['id'])
    if (listings == None): return render_template("profile.html", profile=profile)
    data = []
    for listing in listings:
        data.append({
            'listing': listing,
            'farmer': get_user_by_ID(listing['farmerID'])
        })
    return render_template("profile.html", data=data, profile=profile)

# edit profile
@api_views.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    id = request.args.get('farmerID')
    if (request.method == "POST"):
        data = request.form
        if ('name' in data and not data['name'] == ""):
            set_user_shopname(id, data['name'])

        if ('contact' in data and not data['contact'] == ""):
            set_user_contact(id, data['contact'])

        if ('location' in data and not data['location'] == ""):
            set_user_location(id, data['location'])
        
        if ('image' in request.files and request.files['image'].filename):
            image = request.files['image']
            filename = secure_filename(image.filename)
            path = os.path.realpath( os.path.realpath("App/static/uploaded") + "/" + filename)
            status = image.save(path, image.content_length)
            set_user_photo(id, "static/uploaded/"+filename)
        return redirect('/profile')

    if (request.method == "GET"):
        return render_template("editprofile.html")

# allows the text editor to fetch the saved image from server,
# note that this is not private
# @api_views.route('/images/<filename>')
# def get_image(filename):
#     return send_from_directory("..images/", filename)

