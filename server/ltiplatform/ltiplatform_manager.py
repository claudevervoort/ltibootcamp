from time import time
from copy import copy
from keys.keys_manager import get_client_key, keys, get_keyset, get_public_key
from course.course_manager import Course
from ltiplatform.tool import Tool
from ltiplatform.ltiutil import fc, scope, hmac_sha256_signature


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
        updated[fc('tool_platform')] = {
            'name': self.name,
            'guid': self.guid
        }
        return updated

    def get_keyset(self):
        return get_keyset()

    def get_tool(self, tool_id):
        return next(t for t in self.tools if t.client_id == tool_id)

    def new_tool(self, public_key_pem=None, redirect_uris=None):
        client_id = str(len(self.tools))
        tool = Tool(self, client_id, public_key_pem=public_key_pem, redirect_uris=redirect_uris)
        self.tools.append(tool)
        return tool

    def new_course(self):
        course = Course("LTI Bootcamp Course")
        self.courses[course.id] = course
        return course

    def get_course(self, course_id):
        return self.courses[course_id]
