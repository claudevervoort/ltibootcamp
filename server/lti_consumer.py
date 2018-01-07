from flask import Flask, jsonify
from keys.keys_manager import get_keyset

app = Flask(__name__)

@app.route("/")
def hello():
    return "LTI Bootcamp Tool Consumer, hello!"

@app.route("/.well-known/jwks.json")
def keyset():
    return jsonify(get_keyset())

