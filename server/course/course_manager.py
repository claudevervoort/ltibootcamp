from users.user_manager import Roster
import uuid
from time import time

class LineItem(object):

    def __init__(self, maximum, label, resource_id, tag):
        self.score_maximum = maximum
        self.label = label
        self.resource_id = resource_id
        self.tag = tag
        self.results = []

    @classmethod
    def from_json(cls, li, label=''):
        label = li.get('label', label)
        score_maximum = li['scoreMaximum']
        resource_id = li.get('resourceId', '')
        tag = li.get('tag', '')
        return cls(score_maximum, label, resource_id, tag)

    def getScaledResult(self, user_id):
        return ''


class ResourceLink(object):

    def __init__(self, label, description, url, params, lineitem=None):
        self.label = label
        self.id = str(uuid.uuid1())
        self.description = description
        self.url = url
        self.lineitem = lineitem
        self.params = params

    def addToMessage(self, message):
        return message


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
                self.lineitems.append(rl.lineitem)
            self.links.append(rl)

    def getOneGradableLinkId(self):
        gradables = list(filter(lambda r: r.lineitem, self.links))
        if (gradables):
            return gradables[0].id
        raise Exception("no gradable resource link")
        
    def getResourceLink(self, rlid):
        match = list(filter(lambda r: r.id == rlid, self.links))
        if (match):
            return match[0]
        raise KeyError('No such link ' + rlid)
            