import os
import logging as log
from flask import *
import requests

app = Flask(__name__, static_url_path='/static')

@app.route('/classify', methods=['POST'])
def classify():
    request_data = request.get_data()
    if (request_data != ""):
        result = requests.post("https://us-central1-fuzzylabs.cloudfunctions.net/function-1", request_data)
        return result.text
    else:
        return "No image supplied", 400

@app.route('/')
def home():
    return render_template('index.html')
