import unittest
from methods import rot13_encrypt, rot13_decrypt


class MyTestCase(unittest.TestCase):
    def test_encrypt(self):
        self.assertEqual(rot13_encrypt('Hello world'), 'Uryyb jbeyq')

    def test_decrypt(self):
        self.assertEqual(rot13_encrypt('Uryyb jbeyq'), 'Hello world')


if __name__ == '__main__':
    unittest.main()
