import os
import logging as log
from flask import *
from classifier import Classifier

# test

classifier = Classifier(os.environ['GCP_PROJECT'], None)

def classify(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    request_data = request.get_data()
    if (request_data != ""):
        result = classifier.classify(request_data)
        log.info("Image classification is"  + str(result.classification))
        return result.toJson()
    else:
        return "No image supplied", 400
