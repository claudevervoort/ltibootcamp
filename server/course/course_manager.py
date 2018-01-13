from users import user_manager;
import uuid;

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

    def __init__(self, id, name, roster):
        self.id = id;
        self.context = {
            'id': id,
            'label': name,
            'title': name,
            'type': ['CourseSection']
        }
        self.roster = roster
        self.lineitems = []
        self.links = []

def new_course(name):
    roster = user_manager.get_roster()
    return Course(str(uuid.uuid1()), name, roster)
