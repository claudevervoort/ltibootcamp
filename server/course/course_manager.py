from users.user_manager import Roster
import uuid
from time import time

class Result(object):

    def __init__(self, lineitem, user_id, score, max, grading_progress, comment, timestamp):
        self.lineitem = lineitem
        self.user_id = user_id
        self.score = score
        self.max = max
        self.grading_progress = grading_progress
        self.comment = comment

    @classmethod
    def from_score(cls, lineitem, score):
        return cls(lineitem, 
                      score['userId'], 
                      score.get('scoreGiven'), 
                      score.get('scoreMaximum'), 
                      score['gradingProgress'],
                      score.get('comment'),
                      score['timestamp'])

    def to_json(self):
        r = {
            'userId': self.user_id
        }
        if self.score:
            r['resultScore'] = self.scaled_score
            r['resultMaximum'] = self.lineitem.max
        if self.comment:
            r['comment'] = self.comment
        return r

    @property
    def needs_grading(self):
        return self.grading_progress == 'PendingManual'
    
    @property
    def scaled_score(self):
        if self.score:
            if self.max == self.lineitem.max:
                return self.score
            else:
                return self.score/self.max*self.lineitem.max
        return None


class LineItem(object):

    def __init__(self, tool, course, id, maximum, label, resource_id, tag, resource_link = None):
        self.id = id
        self.course = course
        self.tool = tool
        self.max = maximum
        self.label = label
        self.resource_id = resource_id
        self.tag = tag
        self.resource_link = resource_link
        self.results = {}

    def save_score(self, score):
        #check prior value timestamp here
        self.results[score['userId']]=Result.from_score(self, score)

    @property
    def relative_url(self):
        return "/{0}/lineitems/{1}/lineitem".format(self.course.id, self.id)

    @classmethod
    def from_json(cls, tool, course, li, id=1, label='', resource_link=None):
        label = li.get('label', label)
        score_maximum = li['scoreMaximum']
        resource_id = li.get('resourceId', '')
        tag = li.get('tag', '')
        return cls(tool, course, id, score_maximum, label, resource_id, tag, resource_link=resource_link)

    def getScaledResult(self, user_id):
        s = self.results.get(user_id)
        return s.scaled_score if s else None

    def get_json(self, base_url):
        l = {
            'id': '{0}{1}'.format(base_url, self.relative_url),
            'scoreMaximum': self.max
        }
        if self.resource_link:
            l['ltiLinkId'] = self.resource_link.id
        if self.tag:
            l['tag'] = self.tag
        if self.resource_id:
            l['resourceId'] = self.resource_id
        if self.label:
            l['label'] = self.label
        return l

    def update_from_json(self, json):
        self.label = json.get('label', '')
        self.resource_id = json.get('resource_id', None)
        self.tag = json.get('tag', None)
        self.max = json['scoreMaximum']


class ResourceLink(object):

    def __init__(self, tool, label, description, url, params, lineitem=None):
        self.tool = tool
        self.label = label
        self.id = str(uuid.uuid1())
        self.description = description
        self.url = url
        self.lineitem = lineitem
        self.params = params

    def addToMessage(self, message):
        message.update({
            'http://imsglobal.org/lti/resource_link': {
                'id': self.id,
                'title': self.label
            },
            'http://imsglobal.org/lti/custom': self.params
        })
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
        self.roster = Roster.get_random_roster(self)
        self.lineitems = []
        self.links = []

    def addToMessage(self, message):
        message.update({
            'http://imsglobal.org/lti/context': self.context
        })
        return message

    def addResourceLinks(self, tool, content_items):
        for item in content_items:
            label = item.get('title', '')
            description = item.get('text', '')
            url = item.get('url', '')
            custom = item.get('custom', {})
            rl = ResourceLink(tool, label, description, url, custom)
            if 'lineItem' in item:
                rl.lineitem = LineItem.from_json(tool, self, item['lineItem'], id=(len(self.lineitems) + 1), resource_link=rl)
                self.lineitems.append(rl.lineitem)
            self.links.append(rl)

    def getOneGradableLinkId(self):
        gradables = list(filter(lambda r: True if r.lineitem else False, self.links))
        print(self.links)
        if (gradables):
            return gradables[0].id
        raise Exception("no gradable resource link")
        
    def getResourceLink(self, rlid):
        match = list(filter(lambda r: r.id == rlid, self.links))
        if (match):
            return match[0]
        raise KeyError('No such link ' + rlid)

    def get_roster(self):
        return self.roster

    def get_lineitem(self, lineitem_id):
        match = list(filter(lambda r: str(r.id) == str(lineitem_id), self.lineitems))
        if (match):
            return match[0]
        raise KeyError('No such lineitem ' + lineitem_id)

    def add_lineitem(self, tool, json):
        lineitem = LineItem.from_json(tool, self, json, id=(len(self.lineitems) + 1))
        self.lineitems.append(lineitem)
        return lineitem

    def remove_lineitem(self, item_id):
        self.lineitems = list(filter(lambda li: li.id != item_id, self.lineitems))