import numpy as np
from lab2.ByteGF import BitGF, ByteGF
from lab2.utils import text2byte_generator


def _sub_byte(byte: BitGF):
    inv = ~byte
    new_byte = np.full(8, False)
    for i in range(8):
        new_byte[i] = inv[i]
        for j in range(4):
            new_byte[i] = np.logical_xor(new_byte[i], inv[(i + 4 + j) % 8])
    new_byte = BitGF(new_byte) + BitGF.from_bytes('01100011')
    return new_byte


sub_bytes = np.vectorize(_sub_byte)


def shift_rows(matrix: np.array):
    for i in range(4):
        matrix[i] = np.roll(matrix[i], i)
    return matrix


mix_col_poly = ByteGF([BitGF.from_bytes('00000011'),
                       BitGF.from_bytes('00000001'),
                       BitGF.from_bytes('00000001'),
                       BitGF.from_bytes('00000010')])


def mix_columns(matrix: np.array):
    transposed = matrix.transpose()
    for i in range(4):
        transposed[i] = (ByteGF(transposed[i])*mix_col_poly).bytes
    return transposed.transpose()


def add_round_key(matrix: np.array, keys: np.array):
    transposed = matrix.transpose()
    for i in range(4):
        transposed[i] = np.logical_xor(transposed[i], keys[i])
    return transposed.transpose()


def key_expansion(key: np.array):
    t = key[-1]
    t = sub_bytes(t)
    t.bytes = np.roll(t.bytes, 1)
    #TODO finish



if __name__ == '__main__':
    gen = text2byte_generator('olijnik eto kaif')
    a = next(gen)
    print(a)
    print(add_round_key(a, a))
