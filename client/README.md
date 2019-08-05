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

### Run server

```
FLASK_APP=server.py FLASK_ENV=development flask run
```

### Classify image using server

```
curl http://localhost:5000/classify -XPOST --data-binary @'<path to image file>' -H 'Content-Type: application/octet-stream'
```
