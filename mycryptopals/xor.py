def fixed_xor(bytes1, bytes2):
    if len(bytes1) != len(bytes2):
        raise RuntimeError
    result = bytearray()
    for i in range(0, len(bytes1)):
        result.append(bytes1[i] ^ bytes2[i])
    return result


def single_byte_xor(byte_array, key_byte):
    """XOR every byte in 'byte_array' with the 'key_byte'"""
    result = bytearray()
    for i in range(0, len(byte_array)):
        result.append(byte_array[i] ^ key_byte)
    return result


def multi_byte_xor(byte_array, key_bytes):
    """XOR the 'byte_array' with 'key_bytes'"""
    result = bytearray()
    for i in range(0, len(byte_array)):
        result.append(byte_array[i] ^ key_bytes[i % len(key_bytes)])
    return result
