import os
import logging as log
from flask import *
from flask_basicauth import BasicAuth
import requests

app = Flask(__name__, static_url_path='/static')
app.config['BASIC_AUTH_USERNAME'] = 'fuzzylabs'
app.config['BASIC_AUTH_PASSWORD'] = 'xpertrule'
basic_auth = BasicAuth(app)
request_url = os.environ.get('BACKEND_URL')

log.basicConfig(level=log.INFO)
log.info("Backend URL: " + str(request_url))

@app.route('/classify', methods=['POST'])
@basic_auth.required
def classify():
    request_data = request.get_data()
    if (request_data != ""):
        result = requests.post("https://" + request_url, request_data)
        return result.text
    else:
        return "No image supplied", 400

@app.route('/')
@basic_auth.required
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
