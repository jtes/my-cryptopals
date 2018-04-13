import unittest

from mycryptopals.base64 import bytes_to_base64
from mycryptopals.utils import hex_to_bytes


class TestSet11(unittest.TestCase):

    def test_set1_1(self):
        """ Set 1 / Challenge 1 - convert bytes represented as hex-string to base64"""
        hex_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
        result = bytes_to_base64(hex_to_bytes(hex_string))
        self.assertEqual(result, "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t")


if __name__ == '__main__':
    unittest.main()
