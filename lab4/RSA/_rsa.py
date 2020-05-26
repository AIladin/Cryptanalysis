from ._util import random_prime, mod_inv
from Crypto.Util.number import GCD
from Crypto.Random.random import randint


def encrypt(e: int, n: int, message: bytes):
    """Encrypt message according to RSA algorithm."""

    x = pow(int.from_bytes(message, 'big'), e, n)
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def decrypt(d: int, n: int, message: bytes):
    """Decrypt message according to RSA algorithm."""

    x = pow(int.from_bytes(message, 'big'), d, n)
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def keygen(byte_len=256):
    """ Generates public and private parameters for RSA.

    'N' -- modulus.
    'e', 'd' -- private and public keys.

    :param byte_len: byte length of 'n'.
    :return: 'N', 'e', 'd'.
    """
    # generate two big prime numbers.
    p = random_prime(byte_len // 2)
    q = random_prime(byte_len // 2)

    # calculate Euler's totient function.
    phi = (p - 1) * (q - 1)

    e = 0  # generate random private key.
    while e == 0 or e > phi or GCD(e, phi) != 1:
        e = randint(16, phi)

    d = mod_inv(e, phi)  # calculate multiplicative inverse.
    assert (e * d) % phi == 1, "Something went wrong."
    return p*q, e, d
