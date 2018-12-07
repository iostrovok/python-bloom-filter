import zlib


def crc32(data):
    return zlib.crc32(data) & 0xffffffff


def bits(size, matrix_list, key):

    for matrix in matrix_list:
        out = one_bits(matrix, size, key)
        yield out


def one_bits(matrix, size, key):

    size_chunk = 1 + len(key) / len(matrix)
    i = 0
    while key:
        chunk, key = key[:size_chunk], key[size_chunk:]
        yield (matrix[i] * (crc32(chunk) % size)) % size
        i += 1
