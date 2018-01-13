from flask import Flask, jsonify
from keys.keys_manager import get_keyset, get_client_key, keys
from random import randrange
import jwt

app = Flask(__name__)
tools = []

@app.route("/")
def hello():
    return "LTI Bootcamp Tool Consumer, hello!"

@app.route("/.well-known/jwks.json")
def keyset():
    return jsonify(get_keyset())

@app.route("/newtool")
def newtool():
    key = get_client_key()
    client_id = str(tools.count())
    deployment_id = "deployment_" + str(tools.count())
    tool = {
        'client_id': client_id,
        'deployment_id': deployment_id,
        'key': key.webkey
    }
    tools.append(tool)
    return jsonify(tool)

@app.route("/tool/<int:tool_id>/studentlaunch")
def student_launch(tool_id):
    key = keys[randrange(0, len(keys))]
    privatekey = key[1].exportKey()
    payload = {'test': 'xxx'}
    return jwt.encode(payload, privatekey, 'RS256')
