from enert.init import *
from enert import *
from Crypto.Cipher import *
from fractions import gcd

class RSA:
    def __init__(self):
        """
        Initialize the object

        Args:
            self: (todo): write your description
        """
        pass
    @classmethod
    def new(cls, p, q):
        """
        Creates a new : class : py : p : class : ~.

        Args:
            cls: (todo): write your description
            p: (todo): write your description
            q: (todo): write your description
        """
        return RSAfactory(p, q)

class RSAfactory:
    def __init__(self, p, q):
        """
        Initialize the private key.

        Args:
            self: (todo): write your description
            p: (int): write your description
            q: (int): write your description
        """
        self.p = p
        self.q = q
        self.public_key, self.private_key = self.generate_keys(self.p, self.q)
    def lcm(self, p, q):
        """
        Compute the lcm ( lcm }.

        Args:
            self: (todo): write your description
            p: (int): write your description
            q: (int): write your description
        """
        return (p * q) // gcd(p, q)
    def generate_keys(self, p, q):
        """
        Generate a new key pair.

        Args:
            self: (todo): write your description
            p: (todo): write your description
            q: (todo): write your description
        """
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
        """
        Encrypts plaintext using the plaintext.

        Args:
            self: (todo): write your description
            plain_text: (todo): write your description
        """
        E, N = self.public_key
        plain_integers = [ord(char) for char in plain_text]
        encrypted_integers = [i ** E % N for i in plain_integers]
        encrypted_text = ''.join(chr(i) for i in encrypted_integers)
        self.encrypted_text = encrypted_text
        return encrypted_text
    def decrypt(self, encrypted_text):
        """
        Decrypts the given encrypted string.

        Args:
            self: (todo): write your description
            encrypted_text: (str): write your description
        """
        D, N = self.private_key
        encrypted_integers = [ord(x) for x in encrypted_text]
        decrypted_intergers = [i ** D % N for i in encrypted_integers]
        decrypted_text = ''.join(chr(i) for i in decrypted_intergers)
        self.decrypted_text = decrypted_text
        return decrypted_text
