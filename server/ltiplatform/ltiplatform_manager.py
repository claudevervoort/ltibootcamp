from time import time

class LTIPlatform(object):

    def __init__(self, host):
        self.name = 'LTI Bootcamp Platform'
        self.description = 'LTI Bootcamp Test Platform'
        self.guid = 'ltibc_at_' + str(int(time()))
        self.contact_email = 'claude.vervoort@gmail.com'
        self.version = '2018JAN01'
        self.url = host
    
    def addToMessage(self, launch):
        # make copies here
        launch['http://imsglobal.org/lti/tool_platform'] = {
            'name': self.name,
            'guid': self.guid
        }
        return launch