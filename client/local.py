import sys
sys.path.append('../functions/classify') # a hack so we can pull the cloud function code in for local testing

import os
import logging as log
from flask import *
from classifier import Classifier

app = Flask(__name__, static_url_path='/static')

@app.route('/classify', methods=['POST'])
def classify():
    request_data = request.get_data()
    if (request_data != ""):
        result = classifier.classify(request_data)
        log.info("Image classification is"  + str(result.classification))
        return result.toJson()
    else:
        return "No image supplied", 400

@app.route('/')
def home():
    return render_template('index.html')

classifier = Classifier(os.environ['GCP_PROJECT'], None)
