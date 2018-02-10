from users.user_manager import Roster
import uuid
from time import time

class LineItem(object):

    def __init__(self, maximumScore, label, resource_id, tag):
        self.maximumScore = maximumScore
        self.label = label
        self.results = []

    @classmethod
    def from_json(cls, li, label=''):
        label = li.get('label', label)
        max_score = li['scoreMaximum']
        resource_id = li.get('resourceId', '')
        tag = li.get('tag', '')
        return cls(max_score, label, resource_id, tag)


class ResourceLink(object):

    def __init__(self, label, description, url, params, lineitem=None):
        self.label = label
        self.id = str(uuid.uuid1())
        self.description = description
        self.url = url
        self.lineitem = lineitem
        self.params = params

class Course(object):

    def __init__(self, name):
        self.id = str(uuid.uuid1())
        self.context = {
            'id': self.id,
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

    def addResourceLinks(self, content_items):
        for item in content_items:
            label = item.get('title', '')
            description = item.get('text', '')
            url = item.get('url', '')
            custom = item.get('custom', {})
            rl = ResourceLink(label, description, url, custom)
            if 'lineItem' in item:
                rl.lineitem = LineItem.from_json(item['lineItem'])
            self.links.append(rl)
    
            