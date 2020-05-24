import numpy as np
from lab2.ByteGF import ByteGF, BitGF


def text2byte_generator(text: str):
    encoded = np.array([BitGF.from_bytes(f"{ord(i):08b}") for i in text])
    if len(encoded) % 16 != 0:
        encoded = np.concatenate((encoded, [BitGF.from_bytes('00000000')]*(16 - len(encoded) % 16)))
    for element in np.split(encoded, len(encoded) // 16):
        yield np.reshape(element, (4, 4)).transpose()


def get_random_chunk():
    return np.array([BitGF.random() for i in range(16)]).reshape(4, 4)


def byte2text(matrix: np.array):
    res = ''
    for chunk in matrix:
        flat = np.transpose(chunk).flatten()
        for byte in flat:
            if byte != BitGF.from_hex('00'):
                res += byte.repr16()
    return res


if __name__ == '__main__':
    pass
