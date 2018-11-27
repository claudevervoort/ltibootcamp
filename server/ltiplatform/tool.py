from time import time
from copy import copy
from keys.keys_manager import get_client_key, keys, get_keyset, get_public_key
import jwt
import uuid
from random import randrange
from ltiplatform.ltiutil import fc, scope

class Tool(object):

    def __init__(self, platform, client_id, public_key_pem=None, redirect_uris=None):
        self.client_id = client_id
        self.deployment_id = "deployment_" + str(client_id)
        self.redirect_uris = redirect_uris
        if public_key_pem:
            self.publickey = get_public_key(public_key_pem)
        else:
            self.key = get_client_key()
            self.publickey = self.key['key'].publickey()
        self.platform = platform

    def getPublicKey(self):
        return self.publickey

    def message(self, messageType, course, member, message, return_url, request_url=None, resource_link=None, nonce=None):
        key = keys[randrange(0, len(keys))]
        privatekey = key[1].exportKey()
        now = int(time())
        root_url = request_url.rstrip('/') if request_url else self.platform.url
        if nonce:
            message['nonce'] = nonce
        message.update({
            'iat': now,
            'exp': now + 60,
            'nonce': str(uuid.uuid1()),
            'iss': root_url,
            'aud': self.client_id,
            fc('deployment_id'): self.deployment_id,
            fc('message_type'): messageType,
            fc('version'): '1.3.0',
            fc('launch_presentation'): {
                "document_target": "iframe",
                "return_url": root_url + return_url
            }
        })
        ags_claim = {
            'scope': [scope('lineitem', s='ags'),scope('score', s='ags'),scope('result.readonly', s='ags')],
            'lineitems': '{0}/{1}/lineitems'.format(root_url, course.id) 
        }
        memberships_claim = {
            'context_memberships_url': '{0}/{1}/memberships'.format(root_url, course.id)
        }
        message = member.addToMessage(message)
        message = course.addToMessage(message)
        
        if resource_link:
            message = resource_link.addToMessage(message)
            if resource_link.lineitem:
                ags_claim['lineitem'] = '{0}/{1}/lineitems/{2}/lineitem'.format(root_url, course.id, resource_link.lineitem.id)

        if fc('custom') in message:
            custom = message[fc('custom')]
            resolvers = [course, member]
            if resource_link:
                resolvers.append(resource_link)
            
            def resolve(item):
                value = item[1]
                for resolver in resolvers:
                    if len(value) == 0 or value[0] != '$':
                        break
                    value = resolver.resolve_param(value, member=member)
                return (item[0], value)
            
            message[fc('custom')] = dict(map(resolve, custom.items()))

        message[fc('endpoint', s='ags')] = ags_claim    
        message[fc('namesroleservice', s='nrps')] = memberships_claim 
        message = self.platform.addToMessage(message)
        return jwt.encode(message, privatekey, algorithm='RS256', headers={'kid':key[0]})

