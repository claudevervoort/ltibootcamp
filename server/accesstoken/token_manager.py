from functools import wraps
import uuid
import base64
from time import time
from flask import request, abort

tokens = {}

class Token:

    def __init__(self, client_id, allowed_scopes):
        self.client_id = client_id
        self.allowed_scopes = allowed_scopes
        self.id = 'tk' + str(uuid.uuid1())
        self.created_time = int(time())

    def check(self, *required_scopes):
        return True

    @property
    def expires_in(self):
        return self.created_time - int(time()) + 3600


def new_token(client_id, allowed_scopes):
    token = Token(client_id, allowed_scopes)
    tokens[token.id] = token
    return token

def check_token(*required_scopes):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(request.headers['Authorization'])
            auth = request.headers.get('Authorization', '').split(' ')
            if len(auth) != 2 or auth[0] != 'Bearer':
                abort(403)
            token = Token('sss', [])
            #token = tokens[base64.b64decode(auth[1]).decode()]
            #if not(token and token.check(required_scopes)):
            #    abort(403)
            print(len(args))
            print(kwargs)
            return func(*args, {**kwargs, 'client_id': token.client_id})
        return wrapper
    return decorator
