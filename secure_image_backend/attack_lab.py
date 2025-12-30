import os
from utils import generate_sha256


def tamper_data(data: bytes):
    tampered = bytearray(data)
    if len(tampered) > 10:
        tampered[5] = (tampered[5] + 50) % 255
    return bytes(tampered)


def compare_hash(original: bytes, modified: bytes):
    return generate_sha256(original), generate_sha256(modified)
