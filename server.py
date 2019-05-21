import os
from flask import Flask, request
from classifier import Classifier

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    return str(classifier.classify(request.get_data()))

classifier = Classifier(os.environ['GOOGLE_PROJECT_ID'], os.environ['GOOGLE_MODEL_ID'])
