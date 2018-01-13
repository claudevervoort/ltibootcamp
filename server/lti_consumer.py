from flask import Flask, jsonify
from keys.keys_manager import get_keyset, get_client_key

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

@app.route("/tool/<int:tool_id>/student_launch")
def student_launch(tool_id):
    return ''