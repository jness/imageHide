#!/usr/bin/env python

from Crypto.Cipher import AES
import Image
import base64
from ast import literal_eval
from getpass import getpass
from glob import glob
import argparse
import os, sys

class Encryption:
    '''A Class for encrypting and decrypting strings'''
    def __init__(self, cipherkey):
        self.padding = '~'
        self.pad = lambda s: s + (16 - len(s) % 16) * self.padding
        self.aes = AES.new(self.pad(cipherkey))
    
    def encrypt(self, data):
        enc = self.aes.encrypt(self.pad(data))
        bvalue = base64.b64encode(enc)
        return bvalue
    
    def decrypt(self, data):
        value = base64.b64decode(data)
        dec = self.aes.decrypt(value)
        plain = dec.rstrip(self.padding)
        return plain
    
class Pix:
    '''A Class for encrypting and decrypting Images'''
    def __init__(self, cipherkey):
        self.encryption = Encryption(cipherkey)
    
    def encrypt(self, filename):
        print 'Encrypting %s as %s.aes' % (filename, filename.split('.')[0])
        im = Image.open(filename)
        data = im.tostring()
        edata = self.encryption.encrypt(data)
        f = open('%s.aes' % filename.split('.')[0], 'wb')
        f.write('%s %s\n' % (im.mode, im.size))
        f.write(edata)
        f.close()
        
    def decrypt(self, filename):
        f = open(filename, 'rb')
        data = f.read().split('\n')
        mode = data[0].split(' ', 1)[0]
        size = literal_eval(data[0].split(' ', 1)[1])
        image = self.encryption.decrypt(data[1])
        new_im = Image.fromstring(mode, size, image)
        return new_im

def main():

    # Simple Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--encrypt', nargs='+', help='Encrypt a file')
    parser.add_argument('--show', nargs='+', help='Show an encrypted a file')
    args = parser.parse_args()

    # Get our cipher key
    key = getpass(prompt='Enter Cipherkey: ')
    pcrypt = Pix(key)

    # Encrypt all images
    if args.encrypt:
        for filename in args.encrypt:
            pcrypt.encrypt(filename)

    # Show all images
    if args.show:
        for filename in args.show:
            image = pcrypt.decrypt(filename)
            image.show()

    
if __name__ == '__main__':
    main()
