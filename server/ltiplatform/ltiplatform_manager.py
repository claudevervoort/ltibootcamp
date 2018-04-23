from time import time
from copy import copy
from keys.keys_manager import get_client_key, keys, get_keyset
import jwt
import uuid
from course.course_manager import Course 
from random import randrange
from ltiplatform.ltiutil import fc

class Tool(object):

    def __init__(self, platform, client_id):
        self.client_id = client_id
        self.deployment_id = "deployment_" + str(client_id)
        self.key = get_client_key()
        self.platform = platform

    def getPublicKey(self):
        return self.key['key'].publickey()

    def message(self, messageType, course, member, message, return_url, request_url=None, resource_link=None):
        key = keys[randrange(0, len(keys))]
        privatekey = key[1].exportKey()
        now = int(time())
        root_url = request_url.rstrip('/') if request_url else self.platform.url
        message.update({
            'iat': now,
            'exp': now + 60,
            'nonce': str(uuid.uuid1()),
            'iss': root_url,
            'aud': self.client_id,
            'http://imsglobal.org/lti/deployment_id': self.deployment_id,
            'http://imsglobal.org/lti/message_type': messageType,
            'http://imsglobal.org/lti/version': '1.3.0',
            'http://imsglobal.org/lti/launch_presentation': {
                "document_target": "iframe",
                "return_url": root_url + return_url
            }
        })
        ags_claim = {
            'scope': ["https://imsglobal.org/lti/ags/lineitem",
                        "https://imsglobal.org/lti/ags/result.readonly",
                        "https://imsglobal.org/lti/ags/score"
                        ],
            'lineitems': '{0}/{1}/lineitems'.format(root_url, course.id) 
        }
        memberships_claim = {
            'context_memberships_url': '{0}/{1}/memberships'.format(root_url, course.id)
        }
        message = member.addToMessage(message)
        message = course.addToMessage(message)
        
        if resource_link:
            message = resource_link.addToMessage(message)
            if resource_link.lineitem:
                ags_claim['lineitem'] = '{0}/{1}/lineitems/{2}/lineitem'.format(root_url, course.id, resource_link.lineitem.id)

        if fc('custom') in message:
            custom = message[fc('custom')]
            resolvers = [course, member]
            if resource_link:
                resolvers.append(resource_link)
            
            def resolve(item):
                value = item[1]
                for resolver in resolvers:
                    if len(value) == 0 or value[0] != '$':
                        break
                    value = resolver.resolve_param(value)
                return (item[0], value)
            
            message[fc('custom')] = dict(map(resolve, custom.items()))

        message['http://imsglobal.org/lti/ags'] = ags_claim    
        message['https://purl.imsglobal.org/lti/claim/namesroleservice'] = memberships_claim 
        message = self.platform.addToMessage(message)
        return jwt.encode(message, privatekey, algorithm='RS256', headers={'kid':key[0]})

class LTIPlatform(object):

    def __init__(self, url):
        self.name = 'LTI Bootcamp Platform'
        self.description = 'LTI Bootcamp Test Platform'
        self.guid = 'ltibc_at_' + str(int(time()))
        self.contact_email = 'claude.vervoort@gmail.com'
        self.version = '2018JAN01'
        self.url = url
        self.courses = {}
        self.tools = []
    
    def addToMessage(self, msg):
        updated = copy(msg)
        updated['http://imsglobal.org/lti/tool_platform'] = {
            'name': self.name,
            'guid': self.guid
        }
        return updated

    def get_keyset(self):
        return get_keyset()
    
    def get_tool(self, tool_id):
        return next(t for t in self.tools if t.client_id == tool_id)

    def new_tool(self):
        client_id = str(len(self.tools))
        tool = Tool(self, client_id)
        self.tools.append(tool)
        return tool

    def new_course(self):
        course = Course("LTI Bootcamp Course")
        self.courses[course.id] = course
        return course

    def get_course(self, course_id):
        return self.courses[course_id]