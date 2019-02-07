"""Unit tests for utility functions"""
import unittest

from mycryptopals.base64 import bytes_to_base64, bytes_from_base64
from mycryptopals.hamming import calc_hamming_distance


class TestUtils(unittest.TestCase):

    def test_to_base64(self):
        self.assertEqual(bytes_to_base64(bytes("Test", "utf-8")), "VGVzdA==")
        self.assertEqual(bytes_to_base64(bytes("Polyfon zwitschernd aßen Mäxchens Vögel Rüben, Joghurt und Quark", "utf-8")),
                         "UG9seWZvbiB6d2l0c2NoZXJuZCBhw59lbiBNw6R4Y2hlbnMgVsO2Z2VsIFLDvGJlbiwgSm9naHVydCB1bmQgUXVhcms=")

    def test_from_base64(self):
        self.assertEqual(bytes_from_base64("VGVzdA==").decode(), "Test")
        self.assertEqual(bytes_from_base64("UG9seWZvbiB6d2l0c2NoZXJuZCBhw59lbiBNw6R4Y2hlbnMgVsO2Z2VsIFLDvGJlbiwgSm9naHVydCB1bmQgUXVhcms=").decode(),
                         "Polyfon zwitschernd aßen Mäxchens Vögel Rüben, Joghurt und Quark")

    def test_hamming(self):
        self.assertEqual(calc_hamming_distance('a'.encode(), 'a'.encode()), 0)
        self.assertEqual(calc_hamming_distance('this is a test'.encode(), 'wokka wokka!!!'.encode()), 37)
