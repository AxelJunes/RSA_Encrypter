
# -*- coding: utf-8 -*-

####################################################################################
#                 RSA ENCRYPTION MICROSERVICE WITH VIGENÈRE CIPHER                 #
####################################################################################

from flask import Flask, render_template, request, redirect, url_for
from math import floor, pow # Square root
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
encrypted_msg = []
public_key = 0
private_key = 0



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

    # Format the messages so that they appear correctly on screen
    ciph_msg = " ".join(ciphered_message)
    rsa_msg = " ".join(encrypted_message)
    dec_msg = " ".join(decrypted_message)

    if request.method == "GET":
        return render_template("encrypted.html", ciphered = ciph_msg, encrypted = rsa_msg)
    if request.method == "POST":
        return render_template("decrypted.html", decrypted = dec_msg, deciphered = deciphered_message)

#-----------------------------------------------------------------------------------
#                                  ENCRYPTION
#-----------------------------------------------------------------------------------

def execute(msg, Charset, seed, n):
    global ciphered_message
    global deciphered_message
    global encrypted_message
    global decrypted_message
    global public_key
    global private_key

    # Cast to Integer
    n = int(n)

    #If n is odd
    if n % 2 != 0:
        n += 1

    # Calculate two strong prime numbers
    lim_superior = int(pow(2, (n+1)/2))
    lim_inferior = int(pow(2, n/2-1))

    primo_seguro1 = 2
    primo_seguro2 = 2
    primo1 = 4
    primo2 = 4

    while not sympy.isprime(primo1) or not sympy.isprime(primo_seguro1) or primo_seguro1 == primo_seguro2:
        primo1 = int(floor(random() * ((lim_superior - lim_inferior) + 1) + lim_inferior))
        if sympy.isprime(primo1):
            primo_seguro1 = 2 * primo1 + 1
            if not sympy.isprime(primo_seguro1):
                primo1 = int(floor(random() * ((lim_superior - lim_inferior) + 1) + lim_inferior))

    lim_superior = int(pow(2, (n - 1) / 2))
    lim_inferior = int(pow(2, (n - 2)/ 2 - 1))
    while not sympy.isprime(primo2) or not sympy.isprime(primo_seguro2) or primo_seguro1 == primo_seguro2:
        primo2 = int(floor(random() * ((lim_superior - lim_inferior) + 1) + lim_inferior))
        if sympy.isprime(primo2):
            primo_seguro2 = 2 * primo2 + 1
            if not sympy.isprime(primo_seguro2):
                primo2 = int(floor(random() * ((lim_superior - lim_inferior) + 1) + lim_inferior))

    mod_n = primo_seguro1 * primo_seguro2

    # Vigenère cipher
    ciphered_message = encrypt_vigenere(msg, Charset, seed)

    key_public(primo_seguro1, primo_seguro2)

    # RSA encryption
    encrypted_message = encrypt_rsa(ciphered_message,mod_n)

    # RSA decryption
    decrypted_message = decrypt_rsa(mod_n)

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
            descifrado = descifrado + Txt[n]
        # Iterate
        n += 1
        c = (c + 1) % len(Seed)
    return descifrado




# RSA

# Generate public and private keys
# Store all possible values in array
def key_public(p, q):
    global public_key
    global private_key

    phi = (p-1) * (q-1)
    i = 3  # While loop counter
    while i < phi-1:
        if phi % i == 0:
            i += 1
            continue
        if phi % i == 1 and i != p and i != q:
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
def encrypt_rsa(msg, n):
    global public_key
    global encrypted_msg
    key = public_key
    #encrypted_msg.append(0);
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
        encrypted_msg.append(k)
        encrypted += str(k)
        # Iterate
        i += 1
    # Encrypted message is each element of "m" encrypted
    return encrypted

# RSA decryption
def decrypt_rsa(n):
    global private_key
    global encrypted_msg

    key = private_key
    decrypted = ""
    i = 0
    while i < len(encrypted_msg):
        ct = encrypted_msg[i]
        k = 1
        j = 0 # While loop counter
        while j < key:
            k = k * ct
            k = k % n
            # Iterate
            j += 1
        decrypted += Charset[k]
        # Iterate
        i += 1
    return decrypted

#-----------------------------------------------------------------------------------
#                                      MAIN
#-----------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run()
