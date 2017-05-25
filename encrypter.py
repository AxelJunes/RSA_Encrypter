
# -*- coding: utf-8 -*-

####################################################################################
#                 RSA ENCRYPTION MICROSERVICE WITH VIGENÉRE CIPHER                 #
####################################################################################

from flask import Flask, render_template, request, redirect, url_for
from math import sqrt # Square root
# from sage.all import * #Sage libraries

app = Flask(__name__)
seed = ""
Charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"
original_text = ""
encrypted_text = ""

@app.route("/", methods=["GET", "POST"])
def encrypt():
    global original_text
    global seed
    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
        original_text = request.form["text"]
        seed = intercambia(original_text)
        encrypted_text = encrypt_vigenere(original_text, Charset, seed)
        return redirect(url_for(".decrypt", text = encrypted_text))

@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    global encrypted_text
    global original_text
    global seed
    if request.method == "GET":
        encrypted_text = request.args.get("text")
        return render_template("encrypted.html", text = encrypted_text)
    if request.method == "POST":
        decrypted_text = decrypt_vigenere(encrypted_text, Charset, seed, original_text)
        return render_template("decrypted.html", text = original_text)

#-----------------------------------------------------------------------------------
#                                  VIGENÈRE
#-----------------------------------------------------------------------------------

def intercambia(texto_plano):
    invertida = ""
    x = len(texto_plano)-1
    while x >= 0:
        invertida = invertida + texto_plano[x]
        x = x - 1
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
            c = c - 1
            cifrado = cifrado + Txt[n]
        # Iterate
        n = n + 1
        c = (c + 1) % len(Seed)

    return cifrado

# Vigenére decryption
def decrypt_vigenere(cifrado, Charset, Seed, Txt):
    descifrado = ""
    n = 0
    c = 0
    while n < len(cifrado):
        if Charset.index(cifrado[n]) != -1:
            tmp = (Charset.index(cifrado[n]) + Charset.index(Seed[n])) % len(Charset)
            if tmp < 0:
                tmp = tmp + len(Charset)
            descifrado = descifrado + Charset[tmp]
        else:
            c = c - 1
            descifrado = descifrado + Txt[n];
        # Iterate
        n = n + 1
        c = (c + 1) % len(Seed)
    return descifrado

#-----------------------------------------------------------------------------------
#                                      RSA
#-----------------------------------------------------------------------------------

#Primality test
# Returns 1 if prime and 0 if not
def primo(x):
    j = sqrt(x)
    i = 2 # While loop counter
    while i <= j:
        if x % i == 0:
            return 0
        # Iterate
        i = i + 1
    return 1

# Generate public and private keys
# Store all possible values in array
def key_public():
    k = 0
    i = 2 # While loop counter
    while i < phi:
        if phi % i == 0:
            continue
        flag = primo(i)
        if (flag == 1) and (i != p) and (i != q):
            e[k] = i
            flag = key_private(e[k])
            if flag > 0:
                d[k] = flag
                k = k + 1
            if k == 99:
                break
        # Iterate
        i = i + 1

def key_private(x):
    k = 1
    while 1:
        k = k + phi
        if k % x == 0:
            return k / x

# RSA encryption
def encrypt_rsa():
    key = e[0]
    i = 0
    length = len(msg)

    while i != length:
        pt = m[i]
        k = 1
        j = 0 # while loop counter
        while j < key:
            k = k * pt
            k = k % n
            # Iterate
            j = j + 1
        temp[i] = k
        en[i] = k
        # Iterate
        i = i + 1
    en[i] = -1
    # Encrypted message is each element of "en" Encrypted
    return ''.join(en)

# RSA decryption
def decrypt_rsa():
    key = d[0]
    i = 0
    while en[i] != -1:
        ct = temp[i]
        k = 1
        j = 0 # while loop counter
        while j < key:
            k = k * ct
            k = k % n
            # Iterate
            j = j + 1
        m[i] = k
        # Iterate
        i = i + 1
    m[i] = -1
    # Decrypted message is each element of "m" decrypted
    return ''.join(m)



#-----------------------------------------------------------------------------------
#                                      MAIN
#-----------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run()
