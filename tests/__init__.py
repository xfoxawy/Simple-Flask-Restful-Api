from app import app
from models import db
import json
from base64 import b64encode
from faker import Faker

test_app = app.test_client()
db.init_app(app)
faker = Faker()


def make_request(url, method="GET", data={}):
    hdr = {
        'authorization': 'Basic ' + b64encode('admin:secret'),
        'Content-Type': 'application/json'
    }
    req = test_app.open(url, method=method, data=json.dumps(data), headers=hdr)
    return req


def teardown():
    db.session.remove()
