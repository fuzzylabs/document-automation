import os
import logging as log
from flask import *
from classifier import Classifier

app = Flask(__name__, static_url_path='/static')

@app.route('/classify', methods=['POST'])
def classify():
    request_data = request.get_data()
    classification = str(classifier.classify(request_data))
    log.info("Image classification is"  + classification)
    return jsonify(classification)

@app.route('/')
def home():
    return render_template('index.html')

classifier = Classifier(os.environ['GOOGLE_PROJECT_ID'], os.environ['GOOGLE_MODEL_ID'])
