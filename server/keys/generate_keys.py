from Crypto.PublicKey import RSA

secret_code = "LTI-Bootcamp"

def add_key(index):
    key = RSA.generate(2048)
    encrypted_key = key.exportKey(passphrase=secret_code, pkcs=8,
                                  protection="scryptAndAES128-CBC")

    file_out = open("rsa_key_" + str(index) + ".bin", "wb")
    file_out.write(encrypted_key)

for i in range(4):
    add_key(i)