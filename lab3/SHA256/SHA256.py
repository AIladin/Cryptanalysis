from .preprocessing import *
from .functions import *


class SHA256:

    block_size = 512
    out_size = 256

    def __init__(self, message):
        self.chunk_gen = split_generator(padding(message))
        self.H, self.K = load_constants()
        self.hash = self._encode()

    def _encode_block(self, w: list):
        """ Encode each block of message according to SHA-256 algorithm.

        :param w: Block which consists of 16 32-bit words.
        """
        for i in range(16, 64):  # expand block.
            w.append(bits_sum(small_sigma1(w[i-2]), w[i-7], small_sigma0(w[i-15]), w[i-16]))

        a, b, c, d, e, f, g, h = self.H

        for i in range(64):  # main compression loop.
            t1 = bits_sum(h, big_sigma1(e), ch(e, f, g), self.K[i], w[i])
            t2 = bits_sum(big_sigma0(a), maj(a, b, c))
            h, g, f, e, d, c, b, a = g, f, e, bits_sum(d, t1), c, b, a, bits_sum(t1, t2)

        self.H = [bits_sum(*t) for t in zip(self.H, [a, b, c, d, e, f, g, h])]

    def _encode(self):
        """ Calculates SHA-256 sum for given message.

        :return: 256-bits sum.
        """
        for block in self.chunk_gen:
            self._encode_block(block)

        return sum(self.H)

    @property
    def hex(self):
        return self.hash.hex

    @property
    def bytes(self):
        return self.hash.tobytes()

    @property
    def aes_128_key_bytes(self):
        return self.hash[128:].tobytes()

    @property
    def aes_128_key_hex_dec(self):
        return self.hex[32:]

    @property
    def bits(self):
        return self.hash
