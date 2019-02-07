"""Calculation of the hamming distance of two strings"""

__single_bit_bytes = [128, 64, 32, 16, 8, 4, 2, 1]


def calc_hamming_distance(a, b):
    """ Calculate the hamming distance between two bytearrays."""

    if not isinstance(a, (bytes, bytearray)) or not isinstance(b, (bytes, bytearray)):
        raise TypeError

    if len(a) == 0 or len(b) == 0 or len(a) != len(b):
        raise ValueError(str(len(a)) + ", " + str(len(b)))

    distance = 0
    for i in range(len(a)):
        for sbb in __single_bit_bytes:
            if a[i] & sbb != b[i] & sbb:
                distance += 1

    return distance
