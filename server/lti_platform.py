from flask import Flask, jsonify
from ltiplatform.ltiplatform_manager import LTIPlatform
from course.course_manager import new_course
from keys import keys_manager
from random import randrange
import jwt

platform = LTIPlatform('http://localhost:5000')
app = Flask(__name__)
course_by_tool = {}

@app.route("/")
def hello():
    return "LTI Bootcamp Tool Consumer, hello!"

@app.route("/.well-known/jwks.json")
def keyset():
    return jsonify(platform.get_keyset())

@app.route("/newtool")
def newtool():
    tool = platform.new_tool()
    course = new_course('LTI Bootcamp Course')
    course_by_tool[tool.client_id] = course
    return jsonify({
        'client_id': tool.client_id,
        'deployment_id': tool.deployment_id,
        'key': tool.key['webkey']
    })

@app.route("/tool/<tool_id>/cisr")
def content_item_launch(tool_id):
    course = course_by_tool[tool_id]
    message = {}
    message = course.roster.get_instructor()['user'].addToMessage(message)
    message = course.addToMessage(message)
    return platform.get_tool(tool_id).token('ContentItenSelectionRequest', message)

@app.route("/tool/<tool_id>/link/<int:link_id>/studentlaunch")
def student_launch(tool_id, link_id):
    key = keys[randrange(0, len(keys))]
    privatekey = key[1].exportKey()
    payload = platform.addToMessage({'test': 'xxx'})
    return jwt.encode(payload, privatekey, 'RS256')
