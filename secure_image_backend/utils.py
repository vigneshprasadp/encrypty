import hashlib

def generate_sha256(data):
    return hashlib.sha256(data).hexdigest()
