# -*- coding: utf-8 -*-
import time
from op import OP


def intercambia(texto_plano):
    invertida = ""
    x = len(texto_plano) - 1
    while x >= 0:
        invertida = invertida + texto_plano[x]
        x -= 1
    return invertida

if __name__ == '__main__':
    # Initialize variables
    ciphered_message = ""
    deciphered_message = ""
    encrypted_message = ""
    decrypted_message = ""
    encrypted_msg = []
    public_key = 0
    private_key = 0

    print(time.strftime("%H:%M:%S"))
    original_message = raw_input("Message: ")
    key_length = int(raw_input("Key length: "))
    seed = intercambia(original_message)

    op = OP(original_message, seed, key_length, ciphered_message, deciphered_message, encrypted_message,
            decrypted_message, encrypted_msg, public_key, private_key)

    op.execute()

    print ("Ciphered message: ", op.ciphered_message)
    print ("Encrypted message: ", op.encrypted_message)
    print ("Decrypted message: ", op.decrypted_message)
    print ("Deciphered message: ", op.deciphered_message)
    print ("Clave privada: ", op.private_key)
    print ("Clave publica: ", op.public_key)

    print(time.strftime("%H:%M:%S"))

