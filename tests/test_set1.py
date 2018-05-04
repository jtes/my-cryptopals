import unittest

from mycryptopals.utils import *
from mycryptopals.xor_decrypt import crack_single_byte_xor


class TestSet11(unittest.TestCase):

    def test_set1_1(self):
        """Set 1 / Challenge 1 - Convert hex to base64"""
        hex_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        result = bytes_to_base64(hex_to_bytes(hex_string))
        self.assertEqual(result, "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t")

    def test_set1_2(self):
        """Set 1 / Challenge 2 - Fixed XOR"""
        hex1 = "1c0111001f010100061a024b53535009181c"
        hex2 = "686974207468652062756c6c277320657965"
        result = bytes_to_hex(xor(hex_to_bytes(hex1), hex_to_bytes(hex2)))
        self.assertEqual(result, "746865206b696420646f6e277420706c6179")

    def test_set1_3(self):
        """Set 1 / Challenge 3 - Single-byte XOR cipher"""
        hex_encrypted = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
        bytes_encrypted = hex_to_bytes(hex_encrypted)
        key_byte = crack_single_byte_xor(bytes_encrypted)
        bytes_decrypted = single_byte_xor(bytes_encrypted, key_byte)
        self.assertEqual(bytes_decrypted.decode(), "Cooking MC's like a pound of bacon");


if __name__ == '__main__':
    unittest.main()
