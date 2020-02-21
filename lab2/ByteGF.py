import numpy as np


class ByteGF:
    def __init__(self, c: np.array):
        assert len(c) == 8, "Wrong byte length."
        self.bytes = c
        assert set(self.bytes) == {True, False} or {True} or {False}, "Wrong byte structure."

    @classmethod
    def from_bytes(cls, byte_str: str):
        return cls(np.array(list(map(lambda x: x == '1', reversed(list(byte_str))))))

    @property
    def degree(self):
        return len(self.bytes)

    def __getitem__(self, item):
        return self.bytes[item]

    def __repr__(self):
        return ''.join((map(lambda x: '1' if x else '0', reversed(self.bytes))))

    def __str__(self):
        if True in self.bytes:
            return '+'.join([f"x^{i-1}" for i in range(self.degree, 1, -1) if self[i-1]]) +\
                   (f'+1' if self[0] else '')
        else:
            return "0"

    def __add__(self, other):
        return ByteGF(np.logical_xor(self.bytes, other.bytes))

    @staticmethod
    def _reduce(this: np.array):
        p = [True, False, False, False, True, True, False, True, True]
        while True:
            this = this[np.where(this)[0][0]:]
            t = np.concatenate((p, np.full((len(this)-len(p),), False)))

            this = np.logical_xor(this, t)
            this = this[np.where(this)[0][0]:]
            if len(this) < 9:
                return np.concatenate((np.full((8 - len(this),), False), this))

    def _naive_mul__(self, other):
        tmp = np.zeros(16, dtype='b')
        for x_d, x in enumerate(self):
            for y_d, y in enumerate(other):
                if x and y:
                    tmp[x_d + y_d] = np.logical_xor(tmp[x_d + y_d], 1)
        return tmp

    def __mul__(self, other):
        c = self._reduce(self._naive_mul__(other)[::-1])
        return ByteGF(c[::-1])

    def __pow__(self, power, modulo=None):
        t = self
        for i in range(power-1):
            t = t*self
        return t

    def __invert__(self):
        return self**254


if __name__ == '__main__':
    a = ByteGF.from_bytes('11000000')
    print(a*~a)
