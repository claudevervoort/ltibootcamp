from functools import wraps
import uuid
import base64
from time import time
from flask import request, abort

tokens = {}

class Token:

    def __init__(self, client_id, allowed_scopes):
        self.client_id = client_id
        self.allowed_scopes = allowed_scopes.split(' ')
        self.id = 'tk' + str(uuid.uuid1())
        self.created_time = int(time())

    def check(self, *required_scopes):
        for scope in required_scopes[0]:
            print(scope)
            if scope in self.allowed_scopes:
                return True
        return False

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
            auth = request.headers.get('Authorization', '').split(' ')
            # the reason for 403 is just for debug, in prod system it should not be explained why
            if len(auth) != 2 or auth[0] != 'Bearer':
                abort(403, 'No Authorization')
            token = tokens[base64.b64decode(auth[1]).decode()]
            if not token:
                abort(403, 'No such token')
            if not token.check(required_scopes):
                print('Scope mismatch')
                abort(403, 'Invalid token - scope')
            return func(*args, **{**kwargs, 'client_id': token.client_id})
        return wrapper
    return decorator
