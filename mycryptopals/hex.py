__hextable = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')


def bytes_to_hex(byte_array):
    """convert bytearray to hex-string"""
    ret = []
    for byte in byte_array:
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
