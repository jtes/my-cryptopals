import unittest

from mycryptopals.base64 import bytes_to_base64
from mycryptopals.utils import hex_to_bytes, xor, bytes_to_hex


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


if __name__ == '__main__':
    unittest.main()
