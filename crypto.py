from Crypto.Cipher import AES
import hashlib
import random
import string


__author__ = 'student'


class AESCipher:

    def __init__(self):
        self.BLOCK_SIZE = 16

    def initialize(self, key):
        IV = 16 * '\x00'
        mode = AES.MODE_CBC
        self.encryptor = AES.new(key,mode,IV=IV)
        self.decryptor = AES.new(key,mode,IV=IV)

    def generateKey(self):
        key = ''.join(random.choice(string.ascii_lowercase) for x in range(16))
        return str(hashlib.sha256(key).digest())

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
    print 'hello world'
    enc = e.encrypt('hello world')
    print enc
    dec = e.decrypt(enc)
    print dec
'''






