# -*- coding: utf-8 -*-
from sympy.ntheory.generate import isprime
from math import pow
from random import randint
from sympy import nextprime


# Respresents the operation of encrypting a message
class OP(object):

    # Constructor
    def __init__(self, msg, seed, key_length, ciphered_message, deciphered_message, encrypted_message,
                 decrypted_message, encrypted_msg, public_key, private_key):
        self.msg = msg
        self.charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"
        self.seed = seed
        self.key_length = key_length
        self.ciphered_message = ciphered_message
        self.deciphered_message = deciphered_message
        self.encrypted_message = encrypted_message
        self.decrypted_message = decrypted_message
        self.encrypted_msg = encrypted_msg
        self.public_key = public_key
        self.private_key = private_key

    def execute(self):
        n = self.key_length
        # Cast to Integer
        n = int(n)

        # If n is odd
        if n % 2 != 0:
            n += 1

        # Calculate two strong prime numbers
        lim_superior = int(pow(2, (n + 1) / 2))
        lim_inferior = int(pow(2, n / 2 - 1))

        primo_seguro1 = 2
        primo_seguro2 = 2
        primo1 = 4
        primo2 = 4

        while not isprime(primo1) or not isprime(primo_seguro1) or primo_seguro1 == primo_seguro2:
            primo1 = nextprime(randint(lim_inferior, lim_superior))
            if isprime(primo1):
                primo_seguro1 = 2 * primo1 + 1

        lim_superior = int(pow(2, (n - 1) / 2))
        lim_inferior = int(pow(2, (n - 2) / 2 - 1))
        while not isprime(primo2) or not isprime(primo_seguro2) or primo_seguro1 == primo_seguro2:
            primo2 = nextprime(randint(lim_inferior, lim_superior))
            if isprime(primo2):
                primo_seguro2 = 2 * primo2 + 1
        mod_n = primo_seguro1 * primo_seguro2

        # Vigenère cipher
        self.ciphered_message = self.encrypt_vigenere()

        self.key_public(primo_seguro1, primo_seguro2)

        # RSA encryption
        self.encrypted_message = self.encrypt_rsa(mod_n)

        # RSA decryption
        self.decrypted_message = self.decrypt_rsa(mod_n)

        # Vigenère decipher
        self.deciphered_message = self.decrypt_vigenere(self.decrypted_message)

    # VIGENÈRE

    # Vigenére encryption
    def encrypt_vigenere(self):
        cifrado = ""
        n = 0
        c = 0
        while n < len(self.msg):
            if self.charset.index(self.msg[n]) != -1:
                tmp = (self.charset.index(self.msg[n]) + self.charset.index(self.seed[c])) % len(self.charset)
                cifrado = cifrado + self.charset[tmp]
            else:
                c -= 1
                cifrado = cifrado + self.msg[n]
            # Iterate
            n += 1
            c = (c + 1) % len(self.seed)

        return cifrado

    # Vigenére decryption
    def decrypt_vigenere(self, cifrado):
        descifrado = ""
        m = 0
        c = 0
        while m < len(cifrado):
            if self.charset.index(cifrado[m]) != -1:
                tmp = (self.charset.index(cifrado[m]) - self.charset.index(self.seed[c])) % len(self.charset)
                if tmp < 0:
                    tmp = tmp + len(self.charset)
                descifrado = descifrado + self.charset[tmp]
            else:
                c -= 1
                descifrado = descifrado + self.msg[m]
            # Iterate
            m += 1
            c = (c + 1) % len(self.seed)
        return descifrado

    # RSA

    # Generate public and private keys
    # Store all possible values in array
    def key_public(self, p, q):
        phi = (p - 1) * (q - 1)
        i = 65537  # While loop counter

        if i != p and i != q:
            e = i
            inverse = self.modinv(e, phi)
            if inverse > self.private_key:
                self.public_key = i
                self.private_key = inverse

    @staticmethod
    def extended_gcd(aa, bb):
        lastremainder, remainder = abs(aa), abs(bb)
        x, lastx, y, lasty = 0, 1, 1, 0
        while remainder:
            lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
            x, lastx = lastx - quotient * x, x
            y, lasty = lasty - quotient * y, y
        return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

    def modinv(self, a, m):
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            raise ValueError
        return x % m

    # RSA encryption
    def encrypt_rsa(self, n):

        i = 0
        encrypted = ""
        while i < len(self.ciphered_message):
            pt = self.charset.index(self.ciphered_message[i])
            k = self.my_pow(pt, self.public_key, n)
            k = k % n
            # Iterate
            self.encrypted_msg.append(k)
            encrypted += str(k)
            # Iterate
            i += 1
        # Encrypted message is each element of "m" encrypted
        return encrypted


    # RSA decryption
    def decrypt_rsa(self, n):
        decrypted = ""
        i = 0
        while i < len(self.encrypted_msg):
            ct = self.encrypted_msg[i]
            k = self.my_pow(ct, self.private_key, n)
            k = k % n
            decrypted += self.charset[k]
            # Iterate
            i += 1
        return decrypted

    @staticmethod
    def my_pow(base, exponente, modulo):
        r = 1
        while exponente > 0:
            if exponente & 1:
                r = (r * base) % modulo
            exponente >>= 1
            base = (base * base) % modulo
        return r
