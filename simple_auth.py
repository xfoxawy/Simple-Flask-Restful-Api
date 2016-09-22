from functools import wraps
from flask import request, Response
from helpers import respond


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    data = {"error": 'Could not verify your access level for that URL. You have to login with proper credentials'}
    status_code = 401
    headers = {'WWW-Authenticate': 'Basic realm="Login Required"'}
    return respond(data=data, status_code=status_code, headers=headers)
 

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
