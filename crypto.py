from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import random
import string


__author__ = 'student'


class AESCipher:

    def __init__(self):
        self.BLOCK_SIZE = 16

    def initialize(self, key):
        mode = AES.MODE_CBC
        print 'cipher key ' + key
        iv = Random.new().read(self.BLOCK_SIZE)
        self.encryptor = AES.new(key,mode,IV=iv)
        self.decryptor = AES.new(key,mode,IV=iv)

    def generateKey(self):
        key = ''.join(random.choice(string.digits) for x in range(16))
        return str(hashlib.sha256(key).hexdigest())[:self.BLOCK_SIZE]

    def encrypt( self, raw ):
        raw = self.pad(raw)
        return self.encryptor.encrypt(raw)

    def decrypt( self, enc ):
        return self.unpad(self.decryptor.decrypt(enc))


    def pad(self,plaintext):
        pad = self.BLOCK_SIZE - (len(plaintext)%self.BLOCK_SIZE)
        return plaintext + chr(pad)*pad

    def unpad(self,plaintext):
        char = plaintext[-1]
        return plaintext[:-ord(char)]

'''
if __name__ == "__main__":
    e = AESCipher()
    key = e.generateKey()
    e.initialize(key)
    print 'hello world'
    enc = e.encrypt('hello world')
    print enc
    dec = e.decrypt(enc)
    print dec
'''









