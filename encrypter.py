# RSA Encryption microservice with Vigenere ciphering

from flask import Flask, render_template, request, redirect, url_for
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
        encrypted_text = cifrar(original_text, Charset, seed)
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
        decrypted_text = descifrar(encrypted_text, Charset, seed, original_text)
        return render_template("decrypted.html", text = original_text)

####################################################################################
#                                  FUNCTIONS                                       #
####################################################################################

def intercambia(texto_plano):
    invertida = ""
    x = len(texto_plano)-1
    while x >= 0:
        invertida = invertida + texto_plano[x]
        x = x - 1
    return invertida

# Cipher
def cifrar(Txt, Charset, Seed):
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
        n = n + 1
        c = (c + 1) % len(Seed)

    return cifrado

# Decipher
def descifrar(cifrado, Charset, Seed, Txt):
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
        n = n + 1
        c = (c + 1) % len(Seed)
    return descifrado


if __name__ == "__main__":
    app.run()
