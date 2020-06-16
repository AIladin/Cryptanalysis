import numpy as np


def f(k):
    """RC4 init"""
    s = np.array(list(range(256)))
    j = 0
    for i in range(256):
        j = (j + s[i] + k[i]) % 256
        s[i], s[j] = s[j], s[i]
    return s


if __name__ == '__main__':
    print(bin(0))
    print(bin(1))

    # key containts only zero bytes
    key = [0 for _ in range(256)]
    key = np.array(list(key))

    # key1 -- copy of key with one bit changed to 1.
    key1 = np.copy(key)
    key1[0] = 1

    # if some cell left unchanged
    if any(f(key) == f(key1)):
        print("Which cells are unchanged :\n", f(key) == f(key1))
        print("Number of unchanged cells :", sum(f(key) == f(key1)))
        print("RC4 init for key :\n", f(key))
        print("RC4 init for key1 :\n", f(key1))
