# Introduction

# Usage

## Prerequisites

* `python`
* `virtualenv`
* `pip`

## Setup

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

## Running

### Environment variables

```
GOOGLE_APPLICATION_CREDENTIALS
GCP_PROJECT
```

### Classify an image

```
python classify.py <input image>
```

### Run server

```
FLASK_APP=server.py FLASK_ENV=development flask run
```

### Classify image using server

```
curl http://localhost:5000/classify -XPOST --data-binary @'<path to image file>' -H 'Content-Type: application/octet-stream'
```
