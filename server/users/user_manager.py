from random import sample, randrange
from copy import copy
from time import time
import uuid

NAMES = [('Tijn', 'Willem'),
         ('Peggie', 'Nikole'),
         ('Fleurette', 'Michel'),
         ('Christal', 'Conchúr'),
         ('Lucia', 'Colette'),
         ('Colby', 'Rona'),
         ('Sander', 'Donald'),
         ('Terell', 'Suz'),
         ('Esther', 'Raphael'),
         ('Horatio', 'Maya'),
         ('Ebba', 'Elisa'),
         ('Amos', 'Thad'),
         ('Linwood', 'Talulla'),
         ('Kara', 'Thrace'),
         ('William', 'Adama'),
         ('Gaius', 'Baltar'),
         ('Sharon', 'Valerii'),
         ('Saul', 'Tigh'),
         ('Galen', 'Tyrol'),
         ('Shouta', 'Akio'),
         ('Dean', 'Wolodymyr'),
         ('Kyou', 'Yevheniya')]

ID_PREFIX = 'LTIBCU_'

USERS = []


class User(object):

    def __init__(self, name, user_id):
        self.name = name
        self.id = user_id
        self.sourced_id = uuid.uuid1()
        self.email = '{0}.{1}@example.com'.format(self.name[0], self.name[1])

    def addToMessage(self, msg):
        updated = copy(msg)
        updated.update({
            'sub': self.id,
            'given_name': self.name[0],
            'family_name': self.name[1],
            'name': self.name[0] + ' ' + self.name[1],
            'email': self.email
        })
        return updated

    @property
    def given_name(self):
        return self.name[0]

    @property
    def family_name(self):
        return self.name[1]

    @property
    def fullname(self):
        return '{0} {1}'.format(self.name[0], self.name[1])


class Member(object):

    def __init__(self, user, role):
        self.user = user
        self.role = role
        self.lastUpdated = time()

    def addToMessage(self, msg):
        updated = self.user.addToMessage(msg)
        updated.update({
            'http://imsglobal.org/lti/roles': [self.role]
        })
        return updated

    def to_json(self, base_url):
        json = {
            "status": "liss:Active",
            "member": {
                "@type": "LISPerson",
                "sourcedId": self.user.sourced_id,
                "userId": self.user.id,
                "email": self.user.email,
                "familyName": self.user.family_name,
                "name": self.user.fullname,
                "givenName": self.user.given_name
            },
            "role": [self.role]
        }
        return json
    
    def resolve_param(self, param, member=None):
        return param


class Roster(object):

    def __init__(self, context, users):
        self.context=context
        self.roster = users
        self._next = 0
        self._limit = ''
        self._role = ''
        self._since = 0

    def copy(self, users, next=0, limit=0, role='', since=0):
        roster = Roster(self.context, users)
        roster._next = next if next<len(self.roster) else 0
        roster._limit = self._limit if limit == 0 else limit
        roster._role = self._role if role == '' else role
        roster._since = self._since if since == 0 else since
        return roster

    @classmethod
    def get_random_roster(cls, context):
        users = []
        for user in sample(USERS, 16):
            users.append(
                Member(user, 'http://purl.imsglobal.org/vocab/lis/v2/membership#Learner'))
        users[0].role = 'http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor'
        users[1].role = 'http://purl.imsglobal.org/vocab/lis/v2/membership/instructor#TeachingAssistant'
        return cls(context, users)


    def getInstructor(self):
        return self.roster[0]

    @property
    def students(self):
        return self.roster[2:]

    def getOneStudent(self):
        return self.roster[randrange(2, len(self.roster))]

    def since(self, timestamp):
        return self.copy(list(filter(lambda u:u.lastUpdated>timestamp, self.roster)), since=timestamp)

    def role(self, role):
        return self.copy(list(filter(lambda u:role in u.role, self.roster)), role=role)
    
    def limit(self, start, size):
        if (start<len(self.roster)):
            return self.copy(self.roster[start:(start+size)], next=start+size, limit=size)
        return self.copy([])

    def to_json(self, base_url):
        memberships_url = '{0}/{1}/memberships'.format(base_url, self.context.id)
        differences_url = '{0}?since={1}'.format(memberships_url, int(time()))
        memberships = list(map(lambda r: r.to_json(base_url), self.roster))
        json = {
            "@context": [
                "http://purl.imsglobal.org/ctx/lis/v2/MembershipContainer",
                {
                    "liss": "http://purl.imsglobal.org/vocab/lis/v2/status#",
                    "lism": "http://purl.imsglobal.org/vocab/lis/v2/membership#"
                }
            ],
            "@type": "Page",
            "@id": memberships_url,
            "differences": differences_url,
            "pageOf": {
                "@type": "LISMembershipContainer",
                "membershipSubject": {
                    "@type": "Context",
                    "contextId": self.context.id,
                    "membership": memberships
                }
            }
        }
        if (self._next>0):
            next_url = '{0}?limit={1}&from={2}'.format(memberships_url, self._limit, self._next)
            if (self.role):
                next_url = '{0}&role={1}'.format(next_url, self._role)  
            json['nextPage'] = next_url
        return json


for index in range(len(NAMES)):
    USERS.append(User(NAMES[index], ID_PREFIX + str(index)))
