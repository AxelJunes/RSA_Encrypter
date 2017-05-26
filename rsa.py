# -*- coding: utf-8 -*-
from math import floor, pow
from random import random
import sympy  # Library for primality test

ciphered_message = ""
deciphered_message = ""
encrypted_message = ""
decrypted_message = ""
public_key = 0
private_key = 0

Charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"

# EXECUTION OF THE ENCRYPTION ALGORITHM

def execute(msg, Charset, seed, n):
    global ciphered_message
    global deciphered_message
    global encrypted_message
    global decrypted_message
    global public_key
    global private_key

    # Cast to Integer
    n = int(n)
    # Calculate two strong prime numbers
    lim_superior = int(pow(2, n/2-1))
    lim_inferior = int(pow(2, (n-1)/2-1))

    primo1 = int(floor(random()*((lim_superior - lim_inferior) + 1) + lim_inferior))
    while sympy.isprime(primo1) == False or primo1 % 2 != 1:
        primo1 = int(floor(random()*((lim_superior - lim_inferior) + 1) + lim_inferior))

    primo2 = int(floor(random()*((lim_superior - lim_inferior) + 1) + lim_inferior))
    while sympy.isprime(primo2) == False or primo2 % 2 != 1 or primo1 == primo2:
        primo2 = int(floor(random()*((lim_superior - lim_inferior) + 1) + lim_inferior))

    modN = primo1 * primo2

    # Vigenère cipher
    ciphered_message = encrypt_vigenere(msg, Charset, seed)

    key_public(modN, primo1, primo2)

    # RSA encryption
    encrypted_message = encrypt_rsa(ciphered_message, modN, public_key)

    # RSA decryption
    decrypted_message = decrypt_rsa(encrypted_message, modN, private_key)

    # Vigenère decipher
    deciphered_message = decrypt_vigenere(decrypted_message, Charset, seed, msg)


# VIGENÈRE

def intercambia(texto_plano):
    invertida = ""
    x = len(texto_plano)-1
    while x >= 0:
        invertida = invertida + texto_plano[x]
        x -= 1
    return invertida

# Vigenére encryption
def encrypt_vigenere(Txt, Charset, Seed):
    cifrado = ""
    n = 0
    c = 0
    while n < len(Txt):
        if Charset.index(Txt[n]) != -1:
            tmp = (Charset.index(Txt[n]) + Charset.index(Seed[n])) % len(Charset)
            cifrado = cifrado + Charset[tmp]
        else:
            c -= 1
            cifrado = cifrado + Txt[n]
        # Iterate
        n += 1
        c = (c + 1) % len(Seed)

    return cifrado

# Vigenére decryption
def decrypt_vigenere(cifrado, Charset, Seed, Txt):
    descifrado = ""
    n = 0
    c = 0
    while n < len(cifrado):
        if Charset.index(cifrado[n]) != -1:
            tmp = (Charset.index(cifrado[n]) - Charset.index(Seed[n])) % len(Charset)
            if tmp < 0:
                tmp = tmp + len(Charset)
            descifrado = descifrado + Charset[tmp]
        else:
            c -= 1
            descifrado = descifrado + Txt[n];
        # Iterate
        n += 1
        c = (c + 1) % len(Seed)
    return descifrado




# RSA

# Generate public and private keys
# Store all possible values in array
def key_public(n, p, q):
    global public_key
    global private_key

    phi = (p-1) * (q-1)
    i = 3  # While loop counter
    while i < phi-1:
        if phi % i == 0:
            i += 1
            continue
        if sympy.isprime(i) and i != p and i != q:
            e = i
            inverse = key_private(e, phi)
            if inverse > private_key:
                public_key = i
                private_key = inverse
        # Iterate
        i += 1

def key_private(x, phi):
    k = 1
    while True:
        k = k + phi
        if k % x == 0:
            return k / x

# RSA encryption
def encrypt_rsa(msg, n, public_key):
    key = public_key
    i = 0
    encrypted = ""
    while(i < len(msg)):
        pt = Charset.index(msg[i])
        k = 1
        j = 0  # While loop counter
        while j < key:
            k = k * pt
            k = k % n
            # Iterate
            j += 1
        encrypted += str(k)
        # Iterate
        i += 1
    # Encrypted message is each element of "m" encrypted
    return encrypted

# RSA decryption
def decrypt_rsa(cadena, n, private_key):
    key = private_key
    decrypted = ""
    i = 0
    while i < len(cadena):
        ct = int(cadena[i])
        k = 1
        j = 0 # While loop counter
        while j < key:
            k = k * ct
            k = k % n
            # Iterate
            j += 1
        decrypted = decrypted + Charset[k]
        # Iterate
        i += 1
    return decrypted

if __name__ == '__main__':
    original_message = raw_input("Message: ")
    key_length = int(raw_input("Key length: "))
    seed = intercambia(original_message)
    execute(original_message, Charset, seed, key_length)

    print "Ciphered message: ", ciphered_message
    print "Encrypted message: ", encrypted_message
    print "Decrypted message: ", decrypted_message
    print "Deciphered message: ", deciphered_message
    print "Clave privada: ", private_key
    print "Clave publica: ", public_key


