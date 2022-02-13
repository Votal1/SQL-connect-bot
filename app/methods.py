from codecs import encode, decode


def rot13_encrypt(plaintext):
    return encode(plaintext, 'rot_13')


def rot13_decrypt(ciphertext):
    return decode(ciphertext, 'rot_13')