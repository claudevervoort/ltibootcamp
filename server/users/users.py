from random import sample

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

users = []

class User:

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.email = '{0}.{1}@example.com'.format(self.name[0], self.name[1])


def get_roster():
    roster = []
    for user in sample(users, 16):
        roster.append({'user': user, 'role': 'http://purl.imsglobal.org/vocab/lis/v2/membership#Learner'})
    roster[0]['role'] = 'http://purl.imsglobal.org/vocab/lis/v2/membership#Instructor'
    roster[1]['role'] = 'http://purl.imsglobal.org/vocab/lis/v2/membership/instructor#TeachingAssistant'
    return roster

for index in range(NAMES.count()):
    users.append(User(NAMES[index], ID_PREFIX + str(index)))