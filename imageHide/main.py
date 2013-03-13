#!/usr/bin/env python

from base64 import b64decode, b64encode
from binascii import hexlify
from Crypto.Cipher import AES
from Crypto.Hash import MD5

import Image
import cStringIO
from getpass import getpass
from glob import glob
import argparse
import os, sys

"""
     We will use OpenSSL to encrypt our images

        openssl aes-256-cbc -a -in image.jpg -out image.aes
"""

class Encryption:
    '''A Class for encrypting and decrypting strings'''
    def __init__(self, cipherkey):
        self.secret = cipherkey
        
    def __openssl_kdf(self, req):
        """We need 32 bytes for the AES key, and 16 bytes for the IV"""
        prev = ''
        while req>0:
            prev = MD5.new(prev+self.secret+self.salt).digest()
            req -= 16
            yield prev
    
    def decrypt(self, data):
        
        encrypted = b64decode(data)
        self.salt = encrypted[8:16]
        self.data = encrypted[16:]
        
        mat = ''.join([ x for x in self.__openssl_kdf(32+16) ])
        key = mat[0:32]
        iv  = mat[32:48]
        
        aes = AES.new(key, AES.MODE_CBC, iv)
        clear = aes.decrypt(self.data)
        f = open('test.jpg', 'wb')
        f.write(clear)
        f.close()
        return clear
    
class Pix:
    '''A Class for encrypting and decrypting Images'''
    def __init__(self, cipherkey):
        self.encryption = Encryption(cipherkey)
    
    def decrypt(self, filename):
        f = open(filename, 'rb')
        data = f.read()
        clear = self.encryption.decrypt(data)
        fileobj = cStringIO.StringIO(clear)
        im = Image.open(fileobj)
        return im
    

def main():

    # Simple Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--show', nargs='+', help='Show an encrypted a file')
    args = parser.parse_args()

    # Get our cipher key
    key = getpass(prompt='Enter Cipherkey: ')
    pcrypt = Pix(key)

    # Show all images
    if args.show:
        for filename in args.show:
            image = pcrypt.decrypt(filename)
            image.show()

    
if __name__ == '__main__':
    main()
