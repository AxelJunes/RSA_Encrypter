
# -*- coding: utf-8 -*-
from op import OP

# RSA ENCRYPTION MICROSERVICE WITH VIGENÈRE CIPHER

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

Charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789"


@app.route("/", methods=["GET", "POST"])
def encrypt():
    if request.method == "GET":
        return render_template("home.html")

    if request.method == "POST":
        # Initialize attributes
        ciphered_message = ""
        deciphered_message = ""
        encrypted_message = ""
        decrypted_message = ""
        encrypted_msg = []
        public_key = 0
        private_key = 0

        original_message = request.form["text"]
        key_length = request.form["key"]
        # Request seed from user
        # If seed is empty, use default seed
        if request.form["seed"] != "":
            seed = request.form["seed"]
        else:
            # Default seed is mirrored message
            seed = intercambia(original_message)

        op = OP(original_message, seed, key_length, ciphered_message, deciphered_message, encrypted_message,
                decrypted_message, encrypted_msg, public_key, private_key)
        # Encrypt the message
        op.execute()
        return redirect(url_for(".decrypt", ciphered_message=op.ciphered_message, encrypted_message=op.encrypted_message,
                                decrypted_message=op.decrypted_message, deciphered_message=op.deciphered_message))


@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "GET":
        # Format the messages so that they appear correctly on screen
        ciph_msg = " ".join(request.args['ciphered_message'])
        rsa_msg = " ".join(request.args['encrypted_message'])
        decryp_msg = " ".join(request.args['decrypted_message'])
        deciph_msg = request.args['deciphered_message']
        return render_template("encrypted.html", ciphered=ciph_msg, encrypted=rsa_msg,
                               decrypted=decryp_msg, deciphered=deciph_msg)
    if request.method == "POST":
        decryp = request.form["decrypt"]
        deciph = request.form["deciph"]
        return render_template("decrypted.html", decrypted=decryp, deciphered=deciph)


# Return mirrored message for default seed
def intercambia(texto_plano):
    invertida = ""
    x = len(texto_plano) - 1
    while x >= 0:
        invertida = invertida + texto_plano[x]
        x -= 1
    return invertida


# MAIN
if __name__ == "__main__":
    app.run()
