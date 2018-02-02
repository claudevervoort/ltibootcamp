from users.user_manager import Roster
import uuid

class LineItem(object):

    def __init__(self):
        self.results = []

class ResourceLink(object):

    def __init__(self, label, description, lineitem):
        self.label = label
        self.id = str(uuid.uuid1())
        self.description = description
        self.lineitem = lineitem

class Course(object):

    def __init__(self, id, name):
        self.id = id
        self.context = {
            'id': id,
            'label': name,
            'title': name,
            'type': ['CourseSection']
        }
        self.roster = Roster()
        self.lineitems = []
        self.links = []

    def addToMessage(self, message):
        message['http://imsglobal.org/lti/context'] = self.context
        return message

def new_course(name):
    return Course(str(uuid.uuid1()), name)
