from flask import Flask, jsonify, request, render_template, redirect, send_from_directory
from ltiplatform.ltiplatform_manager import LTIPlatform
from keys import keys_manager
from random import randrange
import jwt

platform = LTIPlatform('http://localhost:5000')
app = Flask(__name__)
course_by_tool = {}

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route("/")
def hello():
    return "LTI Bootcamp Tool Consumer, hello!"

@app.route("/.well-known/jwks.json")
def keyset():
    return jsonify(platform.get_keyset())

@app.route("/newtool")
def newtool():
    tool = platform.new_tool()
    platform.url = request.url_root
    course_by_tool[tool.client_id] = platform.new_course()
    return jsonify({
        'client_id': tool.client_id,
        'deployment_id': tool.deployment_id,
        'webkey': tool.key['webkey'],
        'webkeyPem': tool.key['key'].exportKey().decode('utf-8')
    })

@app.route("/tool/<tool_id>/cisr")
def content_item_launch(tool_id):
    course = course_by_tool[tool_id]
    instructor = course.roster.getInstructor()
    message = {
        "http://imsglobal.org/lti/deep_linking_request": {
            "accept_media_types": ["application/vnd.ims.lti.v1.ltilink"],
            "accept_presentation_document_targets": [ "iframe", "window"],
            "accept_multiple": True,
            "auto_create": True,
            "data": "op=321&v=44"
        }
    }
    return_url = "/tool/{0}/cir".format(course.id)
    return platform.get_tool(tool_id).token('LTIDeepLinkingRequest', course, instructor, message, return_url, request_url=request.url_root)

@app.route("/tool/<context_id>/cir", methods=['POST'])
def content_item_return(context_id):
    encoded_jwt = request.form['jws_token']
    unverified = jwt.decode(encoded_jwt, verify=False)
    tool = platform.get_tool(unverified['iss'])
    deep_linking_res = jwt.decode(encoded_jwt, 
       key=tool.getPublicKey().exportKey(), 
       algorithms=['RS256'],
       audience=request.url_root.rstrip('/'))
    if ('http://imsglobal.org/lti/content_items' in deep_linking_res):
        content_items = deep_linking_res['http://imsglobal.org/lti/content_items']
        platform.get_course(context_id).addResourceLinks(content_items)
    return redirect('/course/'+context_id, code=302)


@app.route("/tool/<tool_id>/context/<context_id>/studentlaunch")
def student_launch(tool_id, context_id):
    course = platform.get_course(context_id)
    rlid = request.args.get('rlid', course.getOneGradableLinkId() )
    resource_link = course.getResourceLink(rlid)
    return platform.get_tool(tool_id).token('LTIResourceLinkLaunch', 
                                            course, 
                                            course.roster.getOneStudent(), 
                                            {}, 
                                            request.url_root,
                                            request_url=request.url_root,
                                            resource_link=resource_link)


@app.route("/course/<course_id>")
def show_course(course_id):
    return render_template('courseoutline.html', course=platform.get_course(course_id))

@app.route("/course/<course_id>/gradebook")
def show_gradebook(course_id):
    return render_template('gradebook.html', course=platform.get_course(course_id))

@app.route("/auth/token", methods=['POST'])
def get_access_token():
    assertion_jwt = request.form['assertion']
    client_id = jwt.decode(assertion_jwt, verify=False)['iss']
    tool = platform.get_tool(client_id)
    assertion = jwt.decode(assertion_jwt, 
                           tool.getPublicKey().exportKey(), 
                           algorithms=['RS256'],
                           aud='{0}/auth/token'.format(request.url_root.rstrip('/')))
    return jsonify({
        "access_token" : "dkj4985kjaIAJDJ89kl8rkn5",
        "token_type" : "Bearer",
        "expires_in" : 3600
    })

