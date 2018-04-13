__hextable = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')


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
    result = []
    for i in range(0, len(bytes1)):
        result.append(bytes1[i] ^ bytes2[i])
    return result
