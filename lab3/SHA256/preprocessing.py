import pickle
from bitstring import Bits
import os


def load_constants():
    """ Loads initial hash values - "H" and round constants "K".

    :return: (H, K)
    """
    this_dir, this_filename = os.path.split(__file__)
    data_path = os.path.join(this_dir, 'constants.pkl')

    with open(data_path, 'rb') as f:
        constants = pickle.load(f)
    return constants["H"], constants['K']


def padding(message: bytes):
    """ Padding operation for input message described in FIPS for SHA256.
    print(type(BitAdd("0b1")))
    :param message: input message.
    :return: padded message.
    """
    ln = len(message) * 8
    k = (448 - ln - 1) % 512
    pad = b'1' + b'0' * k + bin(ln)[2:].rjust(64, '0').encode()
    message += bytes.fromhex(hex(int(pad, 2))[2:])
    return message


def split_generator(message: bytes):
    """ Split message into 512-bit chunks.

    :param message: message with bit-length multiple of 512.
    :return: generator which yields each chunk.
    """

    assert len(message) % 64 == 0

    for i in range(len(message) // 64):
        chunk = message[i * 64: (i + 1) * 64]
        yield [Bits(chunk[j * 4: (j + 1) * 4]) for j in range(16)]
