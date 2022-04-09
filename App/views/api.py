# from crypt import methods
import json
import os
from flask import Blueprint, redirect, render_template, request, send_from_directory
from sqlalchemy import JSON
from werkzeug.utils import secure_filename

import App

api_views = Blueprint('api_views', __name__, template_folder='../templates')

@api_views.route('/', methods=['GET'])
def get_api_docs():
    return render_template('index.html')

@api_views.route('/save', methods=['POST'])
def post_froala_text():
    data = request.form['content']
    print(data)
    return data

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