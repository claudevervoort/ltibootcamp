from Crypto.PublicKey import RSA
from time import time
from base64 import b64encode, urlsafe_b64encode

prefix = str(int(time()))
keys = []

def base64urlUInt_encode(val):
    bytes = val.to_bytes((val.bit_length() +7) // 8, byteorder='big')
    return urlsafe_b64encode(bytes).decode()

def generate_key(index):
    key = RSA.generate(2048)
    return prefix + "_" + str(index), key

def get_keyset():
    keyset = {'keys':[]}
    for key in keys:
        public_key = key[1].publickey()
        keyset['keys'].append({
            'kty': 'rsa',
            'alg': 'HS256',
            'kid': key[0],
            'use': 'sig',
            'e':  base64urlUInt_encode(public_key.e),
            'n':  base64urlUInt_encode(public_key.n)
        })
    return keyset


def get_client_key():
    key = RSA.generate(2048)
    webkey = {
            'kty': 'RSA',
            'alg': 'RS256',
            'use': 'sig',
            'e': base64urlUInt_encode(key.e),
            'd': base64urlUInt_encode(key.d),
            'n': base64urlUInt_encode(key.n)
    }
    return {
        'key': key,
        'webkey': webkey
    }


for index in range(4):
    keys.append(generate_key(index))
    