from enert.init import *
from enert import *
from Crypto.Cipher import *
from fractions import gcd

class RSA:
    def __init__(self):
        pass
    @classmethod
    def new(cls, p, q):
        return RSAfactory(p, q)

class RSAfactory:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.public_key, self.private_key = self.generate_keys(self.p, self.q)
    def lcm(self, p, q):
        return (p * q) // gcd(p, q)
    def generate_keys(self, p, q):
        N = p * q
        L = self.lcm(p - 1, q - 1)
        for i in range(2, L):
            if gcd(i, L) == 1:
                E = i
                break
        for i in range(2, L):
            if (E * i) % L == 1:
                D = i
                break
        return (E, N), (D, N)
    def encrypt(self, plain_text):
        E, N = self.public_key
        plain_integers = [ord(char) for char in plain_text]
        encrypted_integers = [i ** E % N for i in plain_integers]
        encrypted_text = ''.join(chr(i) for i in encrypted_integers)
        self.encrypted_text = encrypted_text
        return encrypted_text
    def decrypt(self, encrypted_text):
        D, N = self.private_key
        encrypted_integers = [ord(x) for x in encrypted_text]
        decrypted_intergers = [i ** D % N for i in encrypted_integers]
        decrypted_text = ''.join(chr(i) for i in decrypted_intergers)
        self.decrypted_text = decrypted_text
        return decrypted_text
