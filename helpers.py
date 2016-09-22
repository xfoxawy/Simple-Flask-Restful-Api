from string import ascii_uppercase
from random import choice
from time import time
from flask import make_response, jsonify


def generate_unique_account_id():
    return (''.join(choice(str(int(time())) + ascii_uppercase) for i in range(16)))


def respond(data={}, status_code=200, json=True, headers={}):
    res = make_response(jsonify(data), status_code)
    if json:
        res.headers['Content-Type'] = "application/json"
    else:
        res.headers['Content-Type'] = "html/text"

    if len(headers) > 0:
        for key in headers:
            res.headers[key] = headers[key]

    return res
