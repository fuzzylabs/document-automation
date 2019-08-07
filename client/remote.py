import os
import logging as log
from flask import *
import requests

app = Flask(__name__, static_url_path='/static')
request_url = os.environ.get('BACKEND_URL')

@app.route('/classify', methods=['POST'])
def classify():
    request_data = request.get_data()
    if (request_data != ""):
        result = requests.post("https://" + request_url, request_data)
        log.error(result.text)
        return result.text
    else:
        return "No image supplied", 400

@app.route('/')
def home():
    return render_template('index.html')
