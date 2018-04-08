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


class Roster(object):

    def __init__(self, context):
        self.roster = []
        self.context = context
        for user in sample(USERS, 16):
            self.roster.append(
                Member(user, 'http://purl.imsglobal.org/vocab/lis/v2/membership#Learner'))
        self.roster[0].role = 'http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor'
        self.roster[1].role = 'http://purl.imsglobal.org/vocab/lis/v2/membership/instructor#TeachingAssistant'

    def getInstructor(self):
        return self.roster[0]

    @property
    def students(self):
        return self.roster[2:]

    def getOneStudent(self):
        return self.roster[randrange(2, len(self.roster))]

    def to_json(self, base_url):
        memberships_url = '{0}/{1}/memberships'.format(
            base_url, self.context.id)
        differences_url = '{0}?since={1}'.format(memberships_url, time())
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
        return json


for index in range(len(NAMES)):
    USERS.append(User(NAMES[index], ID_PREFIX + str(index)))
