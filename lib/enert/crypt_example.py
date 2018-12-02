import math
from hashlib import *
from base64 import *

from enert import *
from enert.pwn import *
from enert.crypt import AES
from enert.crypt import RSA

import better_exceptions

plain_text = 'Welcome to ようこそ ジャパリパーク！'
plain_text = 'Flag{Th1s_1s_S3cr3t_P4ssw0rd!}'

##===============================================

inf('AES (AES is binary to binary)')
key = b'Hello, I am key.'
iv = b'Hi, I am iv.'

#key, iv, plain_text convert 16byte
key = md5(iv).digest()
iv  = md5(iv).digest()

#encode
encoded = plain_text.encode('utf-8')

#pad (plain_text to 16byte)
paded = pad(encoded, 16)

#encrypt
cipher = AES.new(key, AES.MODE_CBC, iv) #make instance
encrypted = cipher.encrypt(paded)

#decrypt
cipher = AES.new(key, AES.MODE_CBC, iv) #make instance
decrypted = cipher.decrypt(encrypted)

#unpad (16byte to plain_text)
unpaded = unpad(decrypted)

#decode
decoded = unpaded.decode('utf-8')

#output
print('[+]plain_text: ', end='')
print(plain_text)
print('[+]paded:      ', end='')
print(paded)
print('[+]encoded     ', end='')
print(encoded)
print('[+]encrypted:  ', end='')
print(repr(encrypted))
print('[+]decrypted:  ', end='')
print(decrypted)
print('[+]decoded     ', end='')
print(decoded)
print('[+]unpaded:    ', end='')
print(unpaded)

##===============================================

inf('RSA (RSA is text to text)')
p = 101
q = 3259

#encrypt
cipher = RSA.new(p, q) #make instance
encrypted = cipher.encrypt(plain_text)

#decrypt
cipher = RSA.new(p, q) #make instance
decrypted = cipher.decrypt(encrypted)

print('[+]plain_text: ', end='')
print(plain_text)
print('[+]encrypted:  ', end='')
print(encrypted)
print('[+]decrypted:  ', end='')
print(decrypted, end='\n\n')
