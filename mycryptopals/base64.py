__b64table = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
              , 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f'
              , 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'
              , 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/')


def bytes_to_base64(byte_array):
    """convert bytes to base64-string"""
    ret = []
    for i in range(0, len(byte_array), 3):
        bb = bytearray(byte_array[i:i + 3])

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


def bytes_from_base64(base64_string):
    """Convert base64-encoded string back to bytes array"""
    ret = []

    input_bytes = bytes(base64_string, "utf-8")
    for i in range(0, len(input_bytes), 4):
        bb = [__b64table.index(chr(x)) for x in input_bytes[i:i + 4] if chr(x) != "="]

        b = (bb[0] << 2) | (bb[1] & 0b11110000) >> 4
        ret.append(b)
        if len(bb) > 2:
            b = ((bb[1] & 0b00001111) << 4) | (bb[2] & 0b11111100) >> 2
            ret.append(b)
        if len(bb) > 3:
            b = ((bb[2] & 0b00000011) << 6) | (bb[3] & 0b00111111)
            ret.append(b)

    return bytearray(ret)
