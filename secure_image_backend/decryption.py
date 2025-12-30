from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from PIL import Image
import numpy as np
import io


def decrypt_image_aes(enc_data, password):
    key = PBKDF2(password, b"salt_123", dkLen=32)

    iv = enc_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)

    decrypted = cipher.decrypt(enc_data[16:])
    return decrypted


def decrypt_image_shuffle(image_bytes, key):
    image = Image.open(io.BytesIO(image_bytes))
    arr = np.array(image)
    
    # 1. Generate the SAME shuffled indices using the SAME key
    indices = np.arange(arr.shape[0])
    np.random.seed(key)
    np.random.shuffle(indices)
    
    # 2. Find the "Inverse" mapping
    # This tells us: "The row that is now at position X belongs at position Y"
    unshuffle_map = np.zeros_like(indices)
    unshuffle_map[indices] = np.arange(len(indices))
    
    # 3. Apply the inverse map to restore original row order
    decrypted_arr = arr[unshuffle_map]
    
    out = Image.fromarray(decrypted_arr)
    buffer = io.BytesIO()
    out.save(buffer, format="PNG")
    return buffer.getvalue()
