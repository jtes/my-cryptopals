"""Simple implementation of AES 128/192/256 EBC without support of padding"""

"""round constants"""
__RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A, 0x2F]

"""s-box for byte substitution during encryption"""
__SBOX = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
          [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
          [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
          [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
          [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
          [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
          [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
          [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
          [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
          [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
          [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
          [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
          [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
          [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
          [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
          [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

"""inverse s-box for byte substitution during decryption"""
__ISBOX = [[0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
           [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
           [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
           [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
           [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
           [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
           [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
           [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
           [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
           [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
           [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
           [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
           [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
           [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
           [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
           [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]]


def __galois_multiply(a, b):
    """Multiplication in GF(2^8), taken from https://en.wikipedia.org/wiki/Finite_field_arithmetic#C_programming_example"""
    result = 0
    while a != 0 and b != 0:
        if b & 0x01:
            result ^= a
        if a & 0x80 != 0:
            a = (a << 1) ^ 0x11b
        else:
            a <<= 0x01 % 0x100  # modulo 0x100 because byte0 and byte1 are int
        b >>= 0x01
    return result


def __mix_columns_encrypt(data):
    """Multiplication of the input-vector with a fixed matrix in GF(2^8)"""
    assert len(data) == 4
    b0, b1, b2, b3 = data
    return [__galois_multiply(b0, 2) ^ __galois_multiply(b1, 3) ^ __galois_multiply(b2, 1) ^ __galois_multiply(b3, 1),
            __galois_multiply(b0, 1) ^ __galois_multiply(b1, 2) ^ __galois_multiply(b2, 3) ^ __galois_multiply(b3, 1),
            __galois_multiply(b0, 1) ^ __galois_multiply(b1, 1) ^ __galois_multiply(b2, 2) ^ __galois_multiply(b3, 3),
            __galois_multiply(b0, 3) ^ __galois_multiply(b1, 1) ^ __galois_multiply(b2, 1) ^ __galois_multiply(b3, 2)]


def __mix_columns_decrypt(data):
    """Multiplication of the input-vector with a fixed matrix in GF(2^8), inverse of __mix_columns"""
    assert len(data) == 4
    b0, b1, b2, b3 = data
    return [__galois_multiply(b0, 0x0e) ^ __galois_multiply(b1, 0x0b) ^ __galois_multiply(b2, 0x0d) ^ __galois_multiply(b3, 0x09),
            __galois_multiply(b0, 0x09) ^ __galois_multiply(b1, 0x0e) ^ __galois_multiply(b2, 0x0b) ^ __galois_multiply(b3, 0x0d),
            __galois_multiply(b0, 0x0d) ^ __galois_multiply(b1, 0x09) ^ __galois_multiply(b2, 0x0e) ^ __galois_multiply(b3, 0x0b),
            __galois_multiply(b0, 0x0b) ^ __galois_multiply(b1, 0x0d) ^ __galois_multiply(b2, 0x09) ^ __galois_multiply(b3, 0x0e)]


def __sbox_single_byte(byte, sbox):
    """S-Box substitution of a single byte"""
    row = byte // 16
    col = byte % 16
    return sbox[row][col]


def __sbox_bytes(data, sbox):
    """S-Box substitution of a list of bytes"""
    return [__sbox_single_byte(byte, sbox) for byte in data]


def __shift_rows_encrypt(data_block):
    """the rows 1/2/3/4 of the matrix are shifted cyclically to the left by offsets 0/1/2/3"""
    return [data_block[0], data_block[5], data_block[10], data_block[15],
            data_block[4], data_block[9], data_block[14], data_block[3],
            data_block[8], data_block[13], data_block[2], data_block[7],
            data_block[12], data_block[1], data_block[6], data_block[11]]


def __shift_rows_decrypt(data_block):
    """the rows 1/2/3/4 of the matrix are shifted cyclically to the right by offsets 0/1/2/3"""
    return [data_block[0], data_block[13], data_block[10], data_block[7],
            data_block[4], data_block[1], data_block[14], data_block[11],
            data_block[8], data_block[5], data_block[2], data_block[15],
            data_block[12], data_block[9], data_block[6], data_block[3]]


def __xor_bytes(bytes1, bytes2):
    """xor of a list of bytes"""
    assert len(bytes1) == len(bytes2)
    return [bytes1[i] ^ bytes2[i] for i in range(len(bytes1))]


def __rcon_word(word, r):
    """xor of the word (list of 4 bytes) with the "r"th round constant"""
    assert len(word) == 4
    return [word[0] ^ __RCON[r - 1], word[1], word[2], word[3]]


def __rotate_word(word):
    """Left shift of the word (list of 4 bytes) by 1 bit"""
    assert len(word) == 4
    return word[1:] + word[0:1]


def __expand_key(key_bytes, rounds):
    """AES key expansion"""
    # number of words in the key
    n = len(key_bytes) // 4

    # list of words for the round keys, where a word is a list of 4 bytes
    round_key_words = []

    # split original key into words and add to round_key_words
    for i in range(0, n):
        round_key_words.append(list(key_bytes[i * 4:i * 4 + 4]))

    # calculate the remaining round key words
    for i in range(n, (rounds + 1) * 4):
        temp = round_key_words[i - 1]
        if i % n == 0:
            temp = __rotate_word(temp)
            temp = __sbox_bytes(temp, __SBOX)
            temp = __rcon_word(temp, i // n)
        elif n > 6 and i % n == 4:
            temp = __sbox_bytes(temp, __SBOX)
        temp = __xor_bytes(temp, round_key_words[i - n])
        round_key_words.append(temp)

    # flatten the round key words into a list of bytes ...
    round_key_bytes = [x for word in round_key_words for x in word]

    # ... and partition it into chunks of 16 bytes to finally get the round keys
    return [round_key_bytes[i:i + 16] for i in range(0, len(round_key_bytes), 16)]


def __encrypt_block(data_block, round_keys):
    """Encrpytion of a block of data"""
    assert len(data_block) == 16

    # encryption is usually described as a set of matrix operations over the data block (represented as a 4x4 column-major matrix)
    # since i didn't want to implement matrix operations und didn't want to use a library, the operations might look rather "inelegant",
    # because i just access the relevant bytes with their respective index in the data block (which is just a list of bytes)
    # for explanation of the operations see https://en.wikipedia.org/wiki/Advanced_Encryption_Standard

    for i in range(len(round_keys)):
        if i > 0:
            data_block = __sbox_bytes(data_block, __SBOX)  # substitute bytes
            data_block = __shift_rows_encrypt(data_block)  # shift rows
        if 0 < i < len(round_keys) - 1:
            # mix columns - the rows 1/2/3/4 of the matrix are multiplied with a constant matrix
            data_block = __mix_columns_encrypt(data_block[0:4]) + \
                         __mix_columns_encrypt(data_block[4:8]) + \
                         __mix_columns_encrypt(data_block[8:12]) + \
                         __mix_columns_encrypt(data_block[12:])
        data_block = __xor_bytes(data_block, round_keys[i])  # add round key
    return data_block


def __decrypt_block(data_block, round_keys):
    """Decrpytion of a block of data"""
    assert len(data_block) == 16

    # see comments in __encrypt_block regarding matrix operations

    for i in reversed(range(len(round_keys))):
        data_block = __xor_bytes(data_block, round_keys[i])  # add round key
        if len(round_keys) - 1 > i > 0:
            data_block = __mix_columns_decrypt(data_block[0:4]) + \
                         __mix_columns_decrypt(data_block[4:8]) + \
                         __mix_columns_decrypt(data_block[8:12]) + \
                         __mix_columns_decrypt(data_block[12:])
        if i > 0:
            data_block = __shift_rows_decrypt(data_block)  # shift rows
            data_block = __sbox_bytes(data_block, __ISBOX)  # substitute bytes

    return data_block


def __encrypt_ecb(data_bytes, round_keys):
    """Encrypts the data in chunks of 16 bytes"""
    encrypted_bytes = []
    for i in range(0, len(data_bytes) // 16):
        encrypted_bytes += __encrypt_block(data_bytes[(16 * i):(16 * (i + 1))], round_keys)
    return encrypted_bytes


def __decrypt_ecb(data_bytes, round_keys):
    """Decrypts the data in chunks of 16 bytes"""
    decrypted_bytes = []
    for i in range(0, len(data_bytes) // 16):
        decrypted_bytes += __decrypt_block(data_bytes[(16 * i):(16 * (i + 1))], round_keys)
    return decrypted_bytes


def __check_input(key_bytes, data_bytes):
    # check key and determine number of transformation rounds
    if not isinstance(key_bytes, (bytes, bytearray)):
        raise RuntimeError('Key must be bytes or bytearrays')
    if len(key_bytes) == 16:
        rounds = 10
    elif len(key_bytes) == 24:
        rounds = 12
    elif len(key_bytes) == 32:
        rounds = 14
    else:
        raise RuntimeError('Length of key must be key must be 16, 20, 24, 28 or 32 bytes')

    # check data
    if not isinstance(data_bytes, (bytes, bytearray)):
        raise RuntimeError('Data must be bytes or bytearrays')
    if len(data_bytes) % 16 != 0:
        raise RuntimeError('Block size is 128 bits, padding is not supported')

    return rounds


def encrypt_ecb(key_bytes, data_bytes):
    """Encrypts the input bytes with the given key"""
    rounds = __check_input(key_bytes, data_bytes)

    # key expansion
    round_keys = __expand_key(key_bytes, rounds)

    # encrypt
    return bytes(__encrypt_ecb(data_bytes, round_keys))


def decrypt_ecb(key_bytes, data_bytes):
    """Decrypts the input bytes with the given key"""
    rounds = __check_input(key_bytes, data_bytes)

    # key expansion
    round_keys = __expand_key(key_bytes, rounds)

    # encrypt
    return bytes(__decrypt_ecb(data_bytes, round_keys))
