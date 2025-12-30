from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def sign_data(data: bytes, private_key_bytes: bytes):
    private_key = RSA.import_key(private_key_bytes)
    h = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature


def verify_signature(data: bytes, signature: bytes, public_key_bytes: bytes):
    public_key = RSA.import_key(public_key_bytes)
    h = SHA256.new(data)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except:
        return False
