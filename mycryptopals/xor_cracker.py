from mycryptopals.xor import single_byte_xor

english_letter_freq = {'a': 116, 'b': 44, 'c': 52, 'd': 32, 'e': 28, 'f': 40, 'g': 16, 'h': 42, 'i': 73, 'j': 5, 'k': 5, 'l': 24, 'm': 38, 'n': 23, 'o': 76, 'p': 43, 'q': 2,
                       'r': 28, 's': 67, 't': 160, 'u': 12, 'v': 8, 'w': 55, 'x': 1, 'y': 8, 'z': 1}
"""score fore frequency of letters in english text (from Wikipedia, modified)"""


def calculate_score(byte_array):
    """Calculates a score for a byte-stream. The score is based on the assumption that the bytes represent an english text."""
    score = 0
    for byte in byte_array:
        char = chr(byte)
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            score += english_letter_freq[char.lower()]
            pass
        else:
            # no letter - score is not increased
            pass
    return score


def crack_single_byte_xor(byte_array):
    """
    Single-byte XOR-decryption of the input bytes. Returns the single byte with the highest score and the computed score.
    The score is based on the assumption that the bytes represent an english text.
    """
    b0 = -1
    score0 = -1
    for b in range(0, 256):
        decryped = single_byte_xor(byte_array, b)
        score = calculate_score(decryped)
        if score > score0:
            score0 = score
            b0 = b
    return b0, score0
