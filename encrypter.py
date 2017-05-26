
# -*- coding: utf-8 -*-

####################################################################################
#                 RSA ENCRYPTION MICROSERVICE WITH VIGENÈRE CIPHER                 #
####################################################################################

from flask import Flask, render_template, request, redirect, url_for
from math import sqrt, floor, pow # Square root
from random import random
import sympy # Library for primality test

app = Flask(__name__)

Charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"
seed = ""
original_text = ""
key_length = ""
ciphered_message = ""
deciphered_message = ""
encrypted_message = ""
decrypted_message = ""



@app.route("/", methods=["GET", "POST"])
def encrypt():
    global original_text
    global seed
    global ciphered_message
    global deciphered_message
    global encrypted_message
    global decrypted_message

    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
        original_text = request.form["text"]
        key_length = request.form["key"]
        # Request seed form user
        # If seed is empty, use default seed
        if request.form["seed"] != "":
            seed = request.form["seed"]
        else:
            # Default seed is mirrored message
            seed = intercambia(original_text)
        #Encrypt
        execute(original_text, Charset, seed, key_length)
        return redirect(url_for(".decrypt"))

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    global original_text
    global seed
    global ciphered_message
    global deciphered_message
    global encrypted_message
    global decrypted_message

    if request.method == "GET":
        return render_template("encrypted.html", ciphered = ciphered_message, encrypted = encrypted_message)
    if request.method == "POST":
        return render_template("decrypted.html", decipher = deciphered_message, decrypted = decrypted_message)

#-----------------------------------------------------------------------------------
#                                  ENCRYPTION
#-----------------------------------------------------------------------------------

def execute(msg, Charset, seed, n):
    global ciphered_message
    global deciphered_message
    global encrypted_message
    global decrypted_message
    public_key = ""
    private_key = ""

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

    primoSeguro1 = 2 * primo1 + 1
    primoSeguro2 = 2 * primo2 + 1
    modN = primoSeguro1 + primoSeguro2

    # Vigenère cipher
    ciphered_message = encrypt_vigenere(msg, Charset, seed)
    key_public(modN, primoSeguro1, primoSeguro2, public_key, private_key)

    # RSA encryption
    encrypted_message = encrypt_rsa(ciphered_message, modN, public_key)

    # RSA decryption
    decrypted_message = decrypt_rsa(encrypted_message, modN, private_key)

    # Vigenère decipher
    deciphered_message = decrypt_vigenere(decrypted_message, Charset, seed, msg)

#-----------------------------------------------------------------------------------
#                                  VIGENÈRE
#-----------------------------------------------------------------------------------

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
            tmp = Charset.index(cifrado[n]) - Charset.index(Seed[n])
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

#-----------------------------------------------------------------------------------
#                                      RSA
#-----------------------------------------------------------------------------------

# Generate public and private keys
# Store all possible values in array
def key_public(n, p, q, public_key, private_key):
    inverse = 0
    phi = (p-1) * (q-1)
    e = 0
    i = 3 # While loop counter
    while i < phi-1:
        if phi % i == 0:
            continue
        if sympy.isprime(i) and (i != p) and (i != q):
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
        k += phi
        if k % x == 0:
            return k / x

# RSA encryption
def encrypt_rsa(msg, n, public_key):
    key = public_key
    i = 0
    while(i < len(msg)):
        pt = Charset.index(msg[i])
        k = 1
        j = 0 # While loop counter
        while j < key:
            k = k * pt
            k = k % n
            # Iterate
            j += 1
        encrypted_message[i] = k
        # Iterate
        i += 1
    # Encrypted message is each element of "m" encrypted
    return ''.join(encrypted_message)

# RSA decryption
def decrypt_rsa(cadena, n, private_key):
    key = private_key
    i = 0
    while i < len(cadena):
        ct = cadena[i]
        k = 1
        j = 0 # While loop counter
        while j < key:
            k = k * ct
            k = k % n
            # Iterate
            j += 1
        decrypted_message = decrypted_message + Charset[k]
        # Iterate
        i += 1
    return decrypted_message


#-----------------------------------------------------------------------------------
#                                      MAIN
#-----------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run()
