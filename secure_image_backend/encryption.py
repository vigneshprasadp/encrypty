from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from PIL import Image
import numpy as np
import io
import base64


def pad(data):
    while len(data) % 16 != 0:
        data += b" "
    return data


def encrypt_image_aes(image_bytes, password):

    key = PBKDF2(password, b"salt_123", dkLen=32)

    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(image_bytes))

    return cipher.iv + encrypted


def encrypt_image_shuffle(image_bytes, key):
    image = Image.open(io.BytesIO(image_bytes))
    arr = np.array(image)
    
    # 1. Create a list of row indices [0, 1, 2, ..., height-1]
    indices = np.arange(arr.shape[0])
    
    # 2. Shuffle those indices using the secret key
    np.random.seed(key)
    np.random.shuffle(indices)
    
    # 3. Reorder the image rows based on shuffled indices
    shuffled_arr = arr[indices]
    
    out = Image.fromarray(shuffled_arr)
    buffer = io.BytesIO()
    out.save(buffer, format="PNG")
    return buffer.getvalue()
