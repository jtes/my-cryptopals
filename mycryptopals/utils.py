"""
utility functions
    - converting from/to hex
    - base64 encoding
    - xor
"""

__hextable = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')

__b64table = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
              , 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f'
              , 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'
              , 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/')


def bytes_to_hex(bytes):
    """convert bytearray to hex-string"""
    ret = []
    for byte in bytes:
        ret.append(__hextable[byte // 16])
        ret.append(__hextable[byte % 16])
    return "".join(ret)


def hex_to_bytes(hex_string):
    """convert hex-string to bytearray"""
    if len(hex_string) % 2 != 0:
        raise RuntimeError

    ret = bytearray()
    for i in range(0, len(hex_string), 2):
        ret.append(__hextable.index(hex_string[i].lower()) * 16 + __hextable.index(hex_string[i + 1].lower()))

    return ret


def xor(bytes1, bytes2):
    if len(bytes1) != len(bytes2):
        raise RuntimeError
    result = bytearray()
    for i in range(0, len(bytes1)):
        result.append(bytes1[i] ^ bytes2[i])
    return result


def single_byte_xor(bytes, key_byte):
    """XOR every byte in 'bytes' with the 'key_byte'"""
    return xor(bytes, [key_byte] * len(bytes))


def bytes_to_base64(bytes):
    """convert bytes to base64-string"""
    ret = []
    for i in range(0, len(bytes), 3):
        bb = bytearray(bytes[i:i + 3])

        # padding
        padding = 3 - len(bb)
        while len(bb) < 3:
            bb.append(0)

        b0 = bb[0] >> 2
        b1 = ((bb[0] & 0b00000011) << 4) | (bb[1] >> 4)
        b2 = ((bb[1] & 0b00001111) << 2) | (bb[2] >> 6)
        b3 = bb[2] & 0b00111111
        ret.append(__b64table[b0])
        ret.append(__b64table[b1])
        ret.append(__b64table[b2])
        ret.append(__b64table[b3])

        # pad with '=' (otherwise would be 'A')
        if padding == 1:
            ret[-1] = '='
        elif padding == 2:
            ret[-1] = '='
            ret[-2] = '='

    return "".join(ret)
