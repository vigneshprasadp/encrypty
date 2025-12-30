from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes


def encrypt_aes_gcm(data: bytes, password: str):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=200000)

    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    return salt + cipher.nonce + tag + ciphertext


def decrypt_aes_gcm(enc: bytes, password: str):
    salt = enc[:16]
    nonce = enc[16:32]
    tag = enc[32:48]
    ciphertext = enc[48:]

    key = PBKDF2(password, salt, dkLen=32, count=200000)

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
