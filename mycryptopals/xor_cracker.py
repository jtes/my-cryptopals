from mycryptopals.hamming import calc_hamming_distance
from mycryptopals.xor import single_byte_xor, multi_byte_xor

english_letter_freq = {'a': 116, 'b': 44, 'c': 52, 'd': 32, 'e': 28, 'f': 40, 'g': 16, 'h': 42, 'i': 73, 'j': 5, 'k': 5, 'l': 24, 'm': 38, 'n': 23, 'o': 76, 'p': 43, 'q': 2,
                       'r': 28, 's': 67, 't': 160, 'u': 12, 'v': 8, 'w': 55, 'x': 1, 'y': 8, 'z': 1}
"""score fore frequency of letters in english text (from Wikipedia, modified)"""


def calculate_score(byte_array):
    """Calculates a score for a byte-stream. The score is based on the assumption that the bytes represent an english text."""
    score = 0
    for byte in byte_array:
        if byte == 0x0a or byte == 0x0d:
            # line breaks are ok
            pass
        elif byte < 0x20 or byte > 0xc0:
            # these bytes are not ok -> return zero score
            return 0
        else:
            char = chr(byte)
            if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
                score += english_letter_freq[char.lower()]
    return score


def crack_single_byte_xor(data):
    """
    Single-byte XOR-decryption of the input bytes. Returns the single byte with the highest score and the computed score.
    The score is based on the assumption that the bytes represent an english text.
    """
    b0, score0 = -1, -1
    for b in range(0, 256):
        decrypted = single_byte_xor(data, b)
        score = calculate_score(decrypted)
        if score > score0:
            score0, b0 = score, b
    return b0, score0


def crack_repeating_xor(data):
    # try to find the keysize by calculating the average hamming distances of the first 8 blocks per key size
    hamming = []
    for i in range(2, 41):
        d = sum([calc_hamming_distance(data[d * i:(d + 1) * i], data[(d + 1) * i:(d + 2) * i]) for d in range(8)]) / i
        hamming.append((i, d))

    # sort hamming distances
    hamming = sorted(hamming, key=lambda x: x[1])

    # try the top 3, break it, and take the one with the highest score for the decrypted value
    key0, score0 = -1, -1
    for (key_size, _) in hamming[0:3]:
        key = []
        for i in range(key_size):
            block = [data[i] for i in range(i, len(data), key_size)]
            key_byte, _ = crack_single_byte_xor(block)
            key.append(key_byte)
        score = calculate_score(multi_byte_xor(data, key))
        if score > score0:
            key0, score0 = key, score

    return key0
