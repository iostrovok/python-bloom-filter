import time

from random_primes import random_primes
from storage import BloomStorage
from utils import bits


class BloomFilter(BloomStorage):

    _body = []
    _matrix_list = []
    _size = 128
    _count_bits = 16
    _count_parts = 4
    _max_count = 0

    def __init__(self,
                 bits=None,  # bits per key
                 size=None,  # min size of filter
                 count=None,  # expected max count of keys
                 storage_key=None,  # expected max count of keys
                 driver=driver,  # expected max count of keys
                 storage_delay_duration=driver,  # expected max count of keys
                 storage_delay_counter=driver  # expected max count of keys
                 ):

        self._matrix_list = []

        if count:
            self._max_count = count

        self._setup_size(size)
        self._setup_bits(bits)
        self._setup_matrix_list()

        self._body = [0 for x in range(self._size)]

    def __str__(self):
        return repr(self.value)

    def __contains__(self, key):
        return self.get()

    def _setup_bits(self, bits):
        if bits and bits > self._count_bits:
            self._count_bits = self._count_bits * (bits / self._count_bits + 1)

    def _setup_size(self, size):
        if size and size > self._size:
            self._size = self._size * (size / self._size + 1)

    def _setup_matrix_list(self):
        primes = random_primes()
        self._matrix_list = [[primes[i * self._count_bits + j] % self._size
                              for j in range(self._count_parts)] for i in range(self._count_bits)]

    def store(self, what):
        print("------ store --------->>>>>")
        print("what: ", what)
        print("self._body: ", self._body)
        print("------ store ---------<<<<<")

    def get(self, key=''):
        if not key:
            return False

        for one_hash in bits(self._size, self._matrix_list, key):
            for one_bit in one_hash:
                if not self._body[one_bit]:
                    return False

        return True

    def add(self, key):
        has_new = []
        for one_hash in bits(self._size, self._matrix_list, key):
            for one_bit in one_hash:
                if not self._body[one_bit]:
                    has_new.append(one_bit)
                    self._body[one_bit] = 1

        if len(has_new) > 0:
            self.save_to_storage(has_new)
            return True

        return False

    # def update_body(self, values=None):
    #     if not values or not isinstance(values, list) or len(values) == 0:
    #         return

    #     for i in values:
    #         if values[i]:
    #             self._body[i] = values[i]

    def bits(self, key):
        chunks = split_key(self._count_bits, key)

        for i in range(self._count_bits):
            chunks[i] = self._hash_matrix[i] * chunks[i] % self._size

        return chunks
