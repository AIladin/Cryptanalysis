import numpy as np
from lab2.ByteGF import BitGF, ByteGF
from lab2.utils import text2byte_generator
from copy import deepcopy


def _sub_byte(byte: BitGF):
    inv = ~byte
    new_byte = np.full(8, False)

    for i in range(8):
        new_byte[i] = inv[i]
        for j in range(4):
            new_byte[i] = np.logical_xor(new_byte[i], inv[(i + 4 + j) % 8])
    new_byte = BitGF(new_byte) + BitGF.from_bytes('01100011')

    return new_byte


def _inv_sub_byte(byte: BitGF):
    bits = deepcopy(byte.bits)
    byte = BitGF(np.roll(bits, 1)) + \
           BitGF(np.roll(bits, 3)) + \
           BitGF(np.roll(bits, 6))

    new_byte = byte + BitGF.from_bytes('00000101')

    inv = ~new_byte
    return inv


sub_bytes = np.vectorize(_sub_byte)
inv_sub_bytes = np.vectorize(_inv_sub_byte)


def shift_rows(matrix: np.array):
    for i in range(4):
        matrix[i] = np.roll(matrix[i], -i)
    return matrix


def inv_shift_rows(matrix: np.array):
    for i in range(4):
        matrix[i] = np.roll(matrix[i], i)
    return matrix


mix_col_poly = ByteGF([BitGF.from_bytes('00000011'),
                       BitGF.from_bytes('00000001'),
                       BitGF.from_bytes('00000001'),
                       BitGF.from_bytes('00000010')])

inv_mix_col_poly = ByteGF([BitGF.from_hex('0b'),
                           BitGF.from_hex('0d'),
                           BitGF.from_hex('09'),
                           BitGF.from_hex('0e')])


def mix_columns(matrix: np.array, poly=mix_col_poly):
    transposed = matrix.transpose()
    for i in range(4):
        transposed[i] = (poly * ByteGF(transposed[i])).bytes
    return transposed.transpose()


def inv_mix_columns(matrix: np.array):
    return mix_columns(matrix, inv_mix_col_poly)


def add_round_key(matrix: np.array, keys: np.array):
    transposed = matrix.transpose()
    t_keys = keys.transpose()
    for i in range(4):
        transposed[i] = transposed[i] + t_keys[i]
    return transposed.transpose()


def key_expansion(key: np.array, n_r=10):
    key = deepcopy(key.transpose())
    yield key.transpose()
    for i in range(n_r):
        t = key[-1]
        t = np.roll(t, -1)
        t = sub_bytes(t)
        r_con = BitGF.from_bytes('00000010') ** i
        t[0] += r_con
        key[0] = t + key[0]
        for j in range(1, 4):
            key[j] = key[j] + key[j - 1]
        yield key.transpose()


def encrypt(state, key):
    key_schedule = key_expansion(key)
    key = next(key_schedule)
    state = add_round_key(deepcopy(state), key)
    for step in range(9):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        key = next(key_schedule)
        state = add_round_key(state, key)

    state = sub_bytes(state)
    state = shift_rows(state)
    key = next(key_schedule)
    state = add_round_key(state, key)
    return state


def decrypt(state, key):
    key_schedule = reversed([deepcopy(key) for key in key_expansion(key)])
    key = next(key_schedule)
    state = add_round_key(deepcopy(state), key)
    for step in range(9):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        key = next(key_schedule)
        state = add_round_key(state, key)
        state = inv_mix_columns(state)

    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    key = next(key_schedule)
    state = add_round_key(state, key)
    return state


if __name__ == '__main__':
    inp = np.array([
        BitGF.from_hex('32'),
        BitGF.from_hex('43'),
        BitGF.from_hex('f6'),
        BitGF.from_hex('a8'),
        BitGF.from_hex('88'),
        BitGF.from_hex('5a'),
        BitGF.from_hex('30'),
        BitGF.from_hex('8d'),
        BitGF.from_hex('31'),
        BitGF.from_hex('31'),
        BitGF.from_hex('98'),
        BitGF.from_hex('a2'),
        BitGF.from_hex('e0'),
        BitGF.from_hex('37'),
        BitGF.from_hex('07'),
        BitGF.from_hex('34'),
    ]).reshape((4, 4)).transpose()

    key1 = np.array([
        BitGF.from_hex('2b'),
        BitGF.from_hex('7e'),
        BitGF.from_hex('15'),
        BitGF.from_hex('16'),
        BitGF.from_hex('28'),
        BitGF.from_hex('ae'),
        BitGF.from_hex('d2'),
        BitGF.from_hex('a6'),
        BitGF.from_hex('ab'),
        BitGF.from_hex('f7'),
        BitGF.from_hex('15'),
        BitGF.from_hex('88'),
        BitGF.from_hex('09'),
        BitGF.from_hex('cf'),
        BitGF.from_hex('4f'),
        BitGF.from_hex('3c'),
    ]).reshape((4, 4)).transpose()
    print(inp)
    enc = encrypt(inp, key1)
    print(enc)
    decrypted = decrypt(enc, key1)
    print(decrypted == inp)
