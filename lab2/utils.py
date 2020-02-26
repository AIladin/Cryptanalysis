import numpy as np
from lab2.ByteGF import ByteGF, BitGF


def text2byte_generator(text: str):
    encoded = np.array([BitGF.from_bytes(f"{ord(i):08b}") for i in text])
    if len(encoded) % 16 != 0:
        encoded = np.concatenate((encoded, [BitGF.from_bytes('00000000')]*(16 - len(encoded) % 16)))
    for element in np.split(encoded, len(encoded) // 16):
        yield np.reshape(element, (4, 4)).transpose()


def byte2text(matrix: np.array):
    flat = np.transpose(matrix).flatten()
    res = ''
    for byte in flat:
        res += chr(int(repr(byte), 2))
    return res


if __name__ == '__main__':
    pass