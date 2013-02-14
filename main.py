#!/usr/bin/env python

from Crypto.Cipher import AES
from PIL import Image, ImageTk
import base64
from ast import literal_eval
from getpass import getpass
from glob import glob
import Tkinter
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
        im = Image.open(filename)
        data = im.tostring()
        edata = self.encryption.encrypt(data)
        f = open('encrypt_%s.aes' % filename.split('.')[0], 'wb')
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

def button_click_exit_mainloop (event):
    event.widget.quit() # this will cause mainloop to unblock.
    
def image(key):
    pcrypt = Pix(key)
    if os.path.exists(sys.argv[2]):
        if sys.argv[1] == 'encrypt':
            pcrypt.encrypt(sys.argv[2])
        elif sys.argv[1] == 'decrypt':
            im = pcrypt.decrypt(sys.argv[2])
            im.show()
    else:
        raise Exception('%s does not exists' % sys.argv[1])

def main(key):
    pcrypt = Pix(key)
  
    # build the Tkinter GUI window
    root = Tkinter.Tk()
    root.bind("<Button>", button_click_exit_mainloop)
    old_label_image = None
    for filename in glob('*.aes'):
        image1 = pcrypt.decrypt(filename)
        root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
        tkpi = ImageTk.PhotoImage(image1)
        label_image = Tkinter.Label(root, image=tkpi)
        label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
        root.title(filename)
        if old_label_image is not None:
            old_label_image.destroy()
        old_label_image = label_image
        root.mainloop()
    
if __name__ == '__main__':
    key = getpass(prompt='Enter Cipherkey: ')
    if len(sys.argv) == 3:
        image(key)
    else:
        main(key)