from utils import bits, random_primes


class BloomFilter(object):

    _body = []
    _matrix_list = []
    _size = 128
    _count_bits = 8
    _count_parts = 7
    _max_count = 0

    def __init__(self,
                 bits=None,  # bits per key
                 size=None,  # min size of filter
                 count=None  # expected max count of keys
                 ):

        self._body = []
        self._matrix_list = []

        if count:
            self._max_count = count

        self._setup_size(size)
        self._setup_bits(bits)
        self._setup_matrix_list()

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
        for i in range(self._count_bits):
            self._matrix_list[i].append([])
            for j in range(self._count_parts):
                self._matrix_list[i].append(primes[i * self._count_bits + j])

    def get(self, key=''):
        if not key:
            return False

        for i in bits(self._count_bits, self._size, self._matrix_list, key):
            if not self._body[i]:
                return False

        return True

    def add(self, key):
        has_new = []
        for i in bits(self._count_bits, self._size, self._matrix_list, key):
            if not self._body[i]:
                has_new[i] = 1
                self._body[i] = 1

        if len(has_new) > 0:
            self.store(has_new)
            return True

        return False

    def update_body(self, values=None):
        if not values or not isinstance(values, list) or len(values) == 0:
            return

        for i in values:
            if values[i]:
                self._body[i] = values[i]

    def bits(self, key):
        chunks = split_key(self._count_bits, key)

        for i in range(self._count_bits):
            chunks[i] = self._hash_matrix[i] * chunks[i] % self._size

        return chunks
