from bitstring import Bits


def rotl(x: Bits, n: int):
    """ The rotate left (circular left shift) operation.

    :param x: a w-bit word
    :param n: integer
    :return: rotated x
    """
    w = len(x)
    assert 0 <= n < w
    return x << n | x >> w - n


def rotr(x: Bits, n: int):
    """ The rotate right (circular right shift) operation.

    :param x: a w-bit word
    :param n: integer
    :return: rotated x
    """
    w = len(x)
    assert 0 <= n < w
    return x >> n | x << w - n


def shr(x: Bits, n: int):
    """ The right shift operation.

    :param x: a w-bit word
    :param n: integer
    :return: rotated x
    """
    assert 0 <= n < len(x)
    return x >> n


def ch(x: Bits, y: Bits, z: Bits):
    """ Ch function from FIPS for SHA256.

    :param x: w-bit words
    :param y: w-bit words
    :param z: w-bit words
    :return: w-bit word
    """
    return (x & y) ^ ((~x) & z)


def maj(x: Bits, y: Bits, z: Bits):
    """ Maj function from FIPS for SHA256.

    :param x: w-bit words
    :param y: w-bit words
    :param z: w-bit words
    :return: w-bit word
    """
    return (x & y) ^ (x & z) ^ (y & z)


def big_sigma0(x: Bits):
    """Big sigma 0 function from FIPS for SHA256.

    :param x: w-bit word
    :return: w-bit word
    """
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)


def big_sigma1(x: Bits):
    """Big sigma 1 function from FIPS for SHA256.

    :param x: w-bit word
    :return: w-bit word
    """
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)


def small_sigma0(x: Bits):
    """Small sigma 0 function from FIPS for SHA256.

    :param x: w-bit word
    :return: w-bit word
    """
    return rotr(x, 7) ^ rotr(x, 18) ^ shr(x, 3)


def small_sigma1(x: Bits):
    """Small sigma 1 function from FIPS for SHA256.

    :param x: w-bit word
    :return: w-bit word
    """
    return rotr(x, 17) ^ rotr(x, 19) ^ shr(x, 10)


MODULUS = 2 ** 32


def bits_sum(*args, width=8):
    """ Sum of Bits objects as integers modulus 2 ** 32

    :param args: iterable of Bits objects.
     :param width: number of bytes in output.
    :return: w-bit word
    """
    rez = 0
    for bits in args:
        assert isinstance(bits, Bits)
        rez = (rez + bits.intbe) % MODULUS
    return Bits("{0:#0{1}x}".format(rez, width + 2), length=32)
