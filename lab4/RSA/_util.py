from Crypto.Random.random import randint
from math import log, ceil
from Crypto.Random import get_random_bytes


def miller_test(n: int, false_positive_prob=1e-6) -> bool:
    """ Performs a Miller-Rabin prime test.

    :param n: int value to check.
    :param false_positive_prob: probability of false positive error.
    :return: True if number is probable prime False if composite.
    """
    # number of iterations calculated from false positive error probability.
    k = int(ceil(-log(false_positive_prob)/log(4)))

    if n & 0:  # k is even.
        return True

    # find such s and m that n-1 = 2**s * m where m is odd.
    m = n - 1
    s = 0
    while m & 0:
        m = m // 2
        s += 1

    # main loop.
    for j in range(k):
        a = randint(2, n-2)
        b = pow(a, m, n)
        if b != 1 and b != n - 1:
            i = 1
            while i < s and b != n - 1:
                b = pow(b, 2, n)
                if b == 1:
                    return False
                i += 1
            if b != n - 1:
                return False
    return True


def random_prime(byte_len=128, false_positive_prob=1e-6) -> int:
    """ Generates a random probable prime of given byte-length.

    :param byte_len: byte-length of output prime.
    :param false_positive_prob:  probability of false positive error.
    :return: integer: probable prime of given byte-length.
    """

    p = 4
    while not miller_test(p, false_positive_prob):
        p = int.from_bytes(get_random_bytes(byte_len), 'big')
        p |= (1 << byte_len * 8 - 1) | 1
    return p


def e_gcd(a, b):
    """Return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def mod_inv(a, m):
    """Returns modular inverse of 'a' if it exists."""
    g, x, y = e_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
