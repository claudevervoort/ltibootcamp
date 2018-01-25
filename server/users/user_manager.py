from random import sample
from copy import copy

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
        self.email = '{0}.{1}@example.com'.format(self.name[0], self.name[1])

    def addToMessage(self, msg):
        updated = copy(msg)
        updated.update = {
            'sub': self.id,
            'given_name': self.name[0],
            'family_name': self.name[1],
            'name': self.name[0] + ' ' + self.name[1],
            'email': self.email
        }
        return updated

class Roster(object):

    def __init__(self):
        self.roster = []
        for user in sample(USERS, 16):
            roster.append({'user': user, 'role': 'http://purl.imsglobal.org/vocab/lis/v2/membership#Learner'})
        roster[0]['role'] = 'http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor'
        roster[1]['role'] = 'http://purl.imsglobal.org/vocab/lis/v2/membership/instructor#TeachingAssistant'


for index in range(NAMES.count()):
    USERS.append(User(NAMES[index], ID_PREFIX + str(index)))