from functools import wraps
import uuid
from time import time
from flask import request

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
    tokens[token.id, token]
    return token

def check_token(*required_scopes):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
