from time import time
from copy import copy
from keys.keys_manager import get_client_key, keys, get_keyset
import jwt
import uuid
from course.course_manager import Course 
from random import randrange

class Tool(object):

    def __init__(self, platform, client_id):
        self.client_id = client_id
        self.deployment_id = "deployment_" + str(client_id)
        self.key = get_client_key()
        self.platform = platform

    def token(self, messageType, course, member, message, return_url, request_url=None):
        key = keys[randrange(0, len(keys))]
        privatekey = key[1].exportKey()
        now = int(time())
        message['iat'] = now
        message['exp'] = now + 60
        message['nonce'] = str(uuid.uuid1())
        message['iss'] = request_url.rstrip('/') if request_url else self.platform.url
        message['aud'] = self.client_id
        message['http://imsglobal.org/lti/deployment_id'] = self.deployment_id
        message['http://imsglobal.org/lti/message_type'] = messageType
        message['http://imsglobal.org/lti/version'] = '1.3.0'
        message['http://imsglobal.org/lti/launch_presentation'] = {
            "document_target": "iframe",
            "return_url": self.platform.url + return_url
        }
        message = member.addToMessage(message)
        message = course.addToMessage(message)
        
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