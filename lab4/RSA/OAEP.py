from Crypto.Random import get_random_bytes
from bitstring import Bits
from ._rsa import encrypt as rsa_enc, decrypt as rsa_dec


def _encrypt_pre(m: bytes, g, h, k0: int, k1: int):
    """Prepare message for RSA encrypting according to OAEP"""
    assert len(m) * 8 == g.out_size - k1, "The message length is wrong." \
                                          f" Expected {g.out_size - k1} bit-length, got {len(m) * 8}."

    m = Bits(m.ljust(g.out_size // 8, b'\0'))
    assert k0 % 8 == 0, "Please specify k0 to fit full byte."
    r = get_random_bytes(k0 // 8)

    x = m ^ g(r).bits
    y = h(x.bytes).bits ^ Bits(r)

    return (x+y).tobytes()


def _decrypt_pre(m: bytes, g, h, k0: int, k1: int):
    """Prepare crypto-text for RSA decrypting according to OAEP"""
    m = Bits(m)
    # message length does not fit.
    assert len(m) - k0 == g.out_size, "crypto text has been modified."
    x = m[:len(m) - k0]
    y = m[len(m) - k0:]
    r = y ^ h(x.bytes).bits
    padded_m = x ^ g(r.bytes).bits
    out = padded_m[:len(m) - k0 - k1]
    pad = padded_m[len(m) - k0 - k1:]
    # wrong amount of zero bytes in zero pad
    assert not any(pad), "crypto text has been modified."
    return out.tobytes()


def encrypt(e: int, n: int,
            k0: int, k1: int, g, h,
            message: bytes) -> bytes:
    """Encrypt according to RSA-OAEP protocol.

    e, n - RSA parameters.
    k0, k1, g, h - OAEP parameters.
    message - message to be encoded
    """
    return rsa_enc(e, n, _encrypt_pre(message, g, h, k0, k1))


def decrypt(d: int, n: int,
            k0: int, k1: int, g, h,
            message: bytes) -> bytes:
    """Decrypt according to RSA-OAEP protocol.

    e, n - RSA parameters.
    k0, k1, g, h - OAEP parameters.
    message - message to be encoded
    """
    return _decrypt_pre(rsa_dec(d, n, message), g, h, k0, k1)
