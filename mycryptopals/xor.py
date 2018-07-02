def xor(bytes1, bytes2):
    if len(bytes1) != len(bytes2):
        raise RuntimeError
    result = bytearray()
    for i in range(0, len(bytes1)):
        result.append(bytes1[i] ^ bytes2[i])
    return result


def single_byte_xor(byte_array, key_byte):
    """XOR every byte in 'bytes' with the 'key_byte'"""
    return xor(byte_array, [key_byte] * len(byte_array))