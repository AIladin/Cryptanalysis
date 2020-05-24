from bitstring import Bits
from .SHA256 import SHA256


class HMAC:
    def __init__(self, key: bytes, message: bytes, hash_class=SHA256):
        self.hash_class = hash_class
        self.key = self._prepare_key(key)
        self.hash = self._encode(message)

    def _prepare_key(self, key: bytes):
        """ Prepare key according to HMAC algorithm to fit hash block bit-size.

        :param key: key of any size.
        :return: key with bit-length equals "block_size" of hash function.
        """
        if len(key) * 8 > self.hash_class.block_size:
            key = self.hash_class(key).bytes

        return Bits(key.ljust(self.hash_class.block_size // 8, b'\x00'))

    def _encode(self, message: bytes):
        """ Encode message according to HMAC algorithm.

        :param message: message of any size.
        :return:  hash sum with bit-length equals "out_size" of hash function.
        """
        o_pad = self.key ^ Bits('0x' + '5c' * (self.hash_class.block_size // 8))
        i_pad = self.key ^ Bits('0x' + '36' * (self.hash_class.block_size // 8))
        a = o_pad.tobytes() + self.hash_class(i_pad.tobytes() + message).bytes
        return self.hash_class(a)

    @property
    def hex(self):
        return self.hash.hex

    @property
    def bytes(self):
        return self.hash.bytes
