from lab2.AES import encrypt, decrypt
from lab2.utils import text2byte_generator, byte2text, get_random_chunk
import numpy as np
from copy import deepcopy


def cbc_encrypt(stream, key):
    iv = get_random_chunk()
    print(byte2text(iv))
    yield iv
    c = iv
    for chunk in stream:
        c = encrypt(chunk + c, key)
        yield c


def cbc_decrypt(stream, key):
    c = next(stream)
    for chunk in stream:
        decrypted = decrypt(deepcopy(chunk), key) + c
        c = chunk
        yield decrypted


def ctr_encrypt(stream, key):
    for i, chunk in enumerate(stream):
        yield encrypt(next(text2byte_generator(bin(i & 256)[2:])), key) + chunk


def ctr_decrypt(stream, key):
    return ctr_encrypt(stream, key)


if __name__ == '__main__':
    text = "test message for testing CBC stream mod"

    test_key = next(text2byte_generator("TEST KEY FOR ME."))

    encoded = np.array([*text2byte_generator(text), ])
    enc = np.array([*cbc_encrypt(iter(encoded), test_key), ])
    decr = np.array([*cbc_decrypt(iter(enc), test_key), ])
    print(encoded == decr)
    print(byte2text(decr))
