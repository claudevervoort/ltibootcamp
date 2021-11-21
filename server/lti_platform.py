from flask import Flask, jsonify, request, render_template, redirect, send_from_directory, abort
from ltiplatform.ltiplatform_manager import LTIPlatform
from ltiplatform.ltiutil import fdlc
from accesstoken.token_manager import check_token, new_token
import jwt


platform = LTIPlatform('http://localhost:5000')
app = Flask(__name__)
course_by_tool = {}

def url_root():
    return request.url_root.rstrip('/')

@app.route('/assets/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route("/")
def hello():
    return "LTI Bootcamp Tool Consumer, hello!"

@app.route("/ping")
def ping():
    return "pong!"

@app.route("/.well-known/jwks.json")
def keyset():
    return jsonify(platform.get_keyset())

@app.route("/newtool")
def newtool():
    tool = platform.new_tool()
    platform.url = request.url_root
    course_by_tool[tool.client_id] = platform.new_course()
    return jsonify({
        'accesstoken_endpoint': request.url_root.rstrip('/') + '/auth/token',
        'keyset_url': request.url_root.rstrip('/') + '/.well-known/jwks.json',
        'client_id': tool.client_id,
        'webkey': tool.key['webkey'],
        'webkeyPem': tool.key['key'].exportKey().decode('utf-8')
    })

@app.route("/newtool", methods=['POST'])
def newtool_with_public_key():
    tool = platform.new_tool(public_key_pem=request.form['public_key_pem'],
                             redirect_uris=request.form['redirect_uris'].split(','))
    platform.url = request.url_root
    course_by_tool[tool.client_id] = platform.new_course()
    return jsonify({
        'accesstoken_endpoint': request.url_root.rstrip('/') + '/auth/token',
        'keyset_url': request.url_root.rstrip('/') + '/.well-known/jwks.json',
        'client_id': tool.client_id,
        'oidc_auth_endpoint': request.url_root.rstrip('/') + '/auth',
    })


@app.route('/auth', methods=['POST'])
def oidc_authorization():
    login_hint = request.form["login_hint"]
    message_hint = request.form["lti_message_hint"]
    client_id = request.form["client_id"]
    redirect_uri = request.form["redirect_uri"]
    nonce = request.form["nonce"]
    state = request.form["state"]

    tool = platform.get_tool(client_id)
    if not (tool and redirect_uri in tool.redirect_uris):
        abort(403)
    if message_hint == 'deeplink':
        id_token = content_item_launch(client_id, nonce=nonce)
    elif login_hint == 'student':
        (context_id, resource_link_id) = message_hint.split('rlid')
        id_token = student_launch(client_id, 
                                  context_id, 
                                  nonce=nonce, 
                                  resource_link_id=resource_link_id)
    else:
        abort(400)
    return render_template('postauthresponse.html', redirect_uri=redirect_uri, state=state, id_token=id_token.decode('utf-8'))


@app.route("/tool/<tool_id>/deeplinkingmessage")
def content_item_launch(tool_id, nonce=None, redirect_uri=None):
    course = course_by_tool[tool_id]
    instructor = course.roster.getInstructor()
    message = {}
    message[fdlc('deep_linking_settings')] = {
        "accept_types": ["ltiLink"],
        "accept_presentation_document_targets": ["iframe", "window"],
        "accept_multiple": True,
        "auto_create": True,
        "data": "op=321&v=44"
    }
    return_url = "/tool/{0}/dlr".format(course.id)
    return platform.get_tool(tool_id).message('LTIDeepLinkingRequest', course, instructor, message, return_url, nonce=nonce, request_url=request.url_root)

@app.route("/tool/<context_id>/dlr", methods=['POST'])
def content_item_return(context_id):
    encoded_jwt = request.form['jws_token']
    unverified = jwt.decode(encoded_jwt, options={'verify_signature': False})
    tool = platform.get_tool(unverified['iss'])
    deep_linking_res = jwt.decode(encoded_jwt,
       key=tool.getPublicKey().exportKey(), 
       algorithms=['RS256'],
       audience=request.url_root.rstrip('/'))
    if (fdlc('content_items') in deep_linking_res):
        content_items = deep_linking_res[fdlc('content_items')]
        platform.get_course(context_id).addResourceLinks(tool, content_items)
    return redirect('/course/'+context_id, code=302)


@app.route("/tool/<tool_id>/context/<context_id>/studentlaunch")
def student_launch(tool_id, context_id, nonce=None,  resource_link_id=None):
    course = platform.get_course(context_id)
    rlid = resource_link_id or request.args.get('rlid', '' )
    rlid = rlid if rlid else course.getOneGradableLinkId()
    resource_link = course.getResourceLink(rlid)
    return_url = "/tool/{0}/resourcelinkreturn/{1}".format(course.id, rlid)
    return platform.get_tool(tool_id).message('LTIResourceLinkLaunch', 
                                            course, 
                                            course.roster.getOneStudent(), 
                                            {}, 
                                            return_url,
                                            nonce=nonce,
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
    if request.form['client_assertion_type'] != 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer':
        abort(400)
    if request.form['grant_type'] != 'client_credentials':
        abort(400)
    if not request.form.get('scope'):
        abort(400)
    assertion_jwt = request.form['client_assertion']
    client_id = jwt.decode(assertion_jwt, verify=False)['iss']
    tool = platform.get_tool(client_id)
    jwt.decode(assertion_jwt, 
               tool.getPublicKey().exportKey(), 
               algorithms=['RS256'],
               audience='{0}/auth/token'.format(request.url_root.rstrip('/')))
    
    access_token = new_token(client_id, request.form['scope'])
    return jsonify({
        "access_token" : access_token.id,
        "token_type" : "Bearer",
        "expires_in" : access_token.expires_in
    })

def get_and_check_lineitem(context_id, item_id, client_id):
    tool = platform.get_tool(client_id)
    course = platform.get_course(context_id)
    lineitem = course.get_lineitem(item_id)
    if not tool == lineitem.tool:
        abort(403, 'Lineitem does not belong to tool making the request')
    return lineitem

@app.route("/<context_id>/lineitems/<item_id>/lineitem/scores", methods=['POST'])
@check_token('https://purl.imsglobal.org/spec/lti-ags/scope/score')
def save_score(context_id=None, item_id=None, client_id=None):
    # we are not checking media type because the URL is enough of a discriminator
    score = request.get_json()
    lineitem = get_and_check_lineitem(context_id,item_id, client_id)
    lineitem.save_score(score)
    return ''

@app.route("/<context_id>/lineitems/<item_id>/lineitem/results", methods=['GET'])
@check_token('https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly')
def get_results(context_id=None, item_id=None, client_id=None):
    # we are not checking media type because the URL is enough of a discriminator
    lineitem = get_and_check_lineitem(context_id,item_id, client_id)
    results = list(map(lambda r: r[1].to_json(), lineitem.results.items()))
    return jsonify(results)

@app.route("/<context_id>/lineitems/<item_id>/lineitem", methods=['GET'])
@check_token('https://purl.imsglobal.org/spec/lti-ags/scope/lineitem', 'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly')
def get_lineitem(context_id=None, item_id=None, client_id=None):
    # we are not checking media type because the URL is enough of a discriminator
    lineitem = get_and_check_lineitem(context_id,item_id, client_id)
    return jsonify(lineitem.get_json(url_root()))

@app.route("/<context_id>/lineitems/<item_id>/lineitem", methods=['PUT'])
@check_token('https://purl.imsglobal.org/spec/lti-ags/scope/lineitem')
def update_lineitem(context_id=None, item_id=None, client_id=None):
    # we are not checking media type because the URL is enough of a discriminator
    lineitem = get_and_check_lineitem(context_id,item_id, client_id)
    lineitem.update_from_json(request.get_json())
    return jsonify(lineitem.get_json(url_root()))

@app.route("/<context_id>/lineitems/<item_id>/lineitem", methods=['DELETE'])
@check_token('https://purl.imsglobal.org/spec/lti-ags/scope/lineitem')
def delete_lineitem(context_id=None, item_id=None, client_id=None):
    # we are not checking media type because the URL is enough of a discriminator
    lineitem = get_and_check_lineitem(context_id,item_id, client_id)
    lineitem.course.remove_lineitem(item_id)
    return ''

@app.route("/<context_id>/lineitems", methods=['GET'])
@check_token('https://purl.imsglobal.org/spec/lti-ags/scope/lineitem', 'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly')
def get_lineitems(context_id=None, client_id=None):
    # we are not checking media type because the URL is enough of a discriminator
    tool = platform.get_tool(client_id)
    course = platform.get_course(context_id)
    results = list(map(lambda l: l.get_json(url_root()), filter(lambda l: l.tool==tool, course.lineitems)))
    return jsonify(results)

@app.route("/<context_id>/lineitems", methods=['POST'])
@check_token('https://purl.imsglobal.org/spec/lti-ags/scope/lineitem')
def add_lineitem(context_id=None, client_id=None):
    # we are not checking media type because the URL is enough of a discriminator
    tool = platform.get_tool(client_id)
    course = platform.get_course(context_id)
    lineitem = course.add_lineitem(tool, request.get_json())
    return jsonify(lineitem.get_json(url_root()))

@app.route("/<context_id>/memberships", methods=['GET'])
@check_token('https://purl.imsglobal.org/spec/lti-nrps/scope/contextmembership.readonly')
def get_memberships(context_id=None, client_id=None):
    # we are not checking media type because the URL is enough of a discriminator
    tool = platform.get_tool(client_id)
    course = platform.get_course(context_id)
    roster = course.get_roster()
    if ('since' in request.args):
        roster = roster.since(int(request.args['since']))
    if ('role' in request.args):
        roster = roster.role(request.args['role'])
    if ('limit' in request.args):
        start = int(request.args.get('from', '0'))
        limit = int(request.args['limit'])
        roster = roster.limit(start, limit)
    return jsonify(roster.to_json(url_root()))
