from flask import Flask, jsonify
from ltiplatform.ltiplatform_manager import LTIPlatform
from keys.keys_manager import get_keyset, get_client_key, keys
from random import randrange
import jwt

platform = LTIPlatform('http://localhost')
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
    client_id = str(len(tools))
    deployment_id = "deployment_" + str(len(tools))
    tool = {
        'client_id': client_id,
        'deployment_id': deployment_id,
        'key': key['webkey']
    }
    tools.append(tool)
    return jsonify(tool)

@app.route("/tool/<int:tool_id>/cisr")
def content_item_launch(tool_id):
    key = keys[randrange(0, len(keys))]
    privatekey = key[1].exportKey()
    payload = platform.addToMessage({'test': 'xxx'})
    return jwt.encode(payload, privatekey, algorithm='RS256', headers={'kid':key[0]})

@app.route("/tool/<int:tool_id>/link/<int:link_id>/studentlaunch")
def student_launch(tool_id, link_id):
    key = keys[randrange(0, len(keys))]
    privatekey = key[1].exportKey()
    payload = platform.addToMessage({'test': 'xxx'})
    return jwt.encode(payload, privatekey, 'RS256')
