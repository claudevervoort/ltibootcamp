class CryptographicKey(object):

    def __init__(self, )

class Verifiaction(object):

    def __init__(self, type='SignedBadge')

class Criteria(object):

    def __init__(narrative):
        self.narrative=narrative


class Issuer(object):

    def __init__(self, id, name=None, url=None):
        self.id=id
        self.name=name
        self.url=url


class Image(object):

    def __init__(self, id):
        self.id=id


class Badge(object):

    def __init__(self, id, name, description+none, criteria=None, issuer=None, image=None):
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.criteria = criteria
        self.issuer = issuer



'''

{
  "@context": "https://w3id.org/openbadges/v2",
  "id": "https://example.org/assertions/123",
  "type": "Assertion",
  "recipient": {
    "type": "email",
    "identity": "alice@example.org"
  },
  "issuedOn": "2016-12-31T23:59:59+00:00",
  "verification": {
    "type": "hosted"
  },
  "badge": {
    "type": "BadgeClass",
    "id": "https://example.org/badges/5",
    "name": "3-D Printmaster",
    "description": "This badge is awarded for passing the 3-D printing knowledge and safety test.",
    "image": "https://example.org/badges/5/image",
    "criteria": {
      "narrative": "Students are tested on knowledge and safety, both through a paper test and a supervised performance evaluation on live equipment"
    },
    "issuer": {
      "id": "https://example.org/issuer",
      "type": "Profile",
      "name": "Example Maker Society",
      "url": "https://example.org",
      "email": "contact@example.org",
      "verification": {
         "allowedOrigins": "example.org"
      }
    }
  }
}
'''