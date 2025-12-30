from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
import io

from encryption import encrypt_image_aes, encrypt_image_shuffle
from decryption import decrypt_image_aes, decrypt_image_shuffle
from stego_hide import hide_message_in_image
from stego_extract import extract_message
from utils import generate_sha256
from encryption_gcm import encrypt_aes_gcm, decrypt_aes_gcm
from signature import generate_rsa_keys, sign_data, verify_signature
from watermark import add_watermark
from attack_lab import tamper_data, compare_hash
from metrics import execution_time


app = FastAPI(title="SecureVision Backend",
              description="Image Encryption & Steganography API",
              version="1.0")


@app.get("/")
def home():
    return {"message": "SecureVision Backend Running"}


# ========================= IMAGE ENCRYPTION =========================

@app.post("/encrypt/aes")
async def encrypt_aes(image: UploadFile = File(...), password: str = Form(...)):
    img_bytes = await image.read()
    encrypted_data = encrypt_image_aes(img_bytes, password)

    return StreamingResponse(io.BytesIO(encrypted_data),
                             media_type="application/octet-stream",
                             headers={"Content-Disposition": "attachment; filename=encrypted.bin"})


@app.post("/decrypt/aes")
async def decrypt_aes(file: UploadFile = File(...), password: str = Form(...)):
    enc_bytes = await file.read()

    decrypted_img = decrypt_image_aes(enc_bytes, password)

    return StreamingResponse(io.BytesIO(decrypted_img),
                             media_type="image/png",
                             headers={"Content-Disposition": "attachment; filename=decrypted.png"})


# ========================= SHUFFLE ENCRYPTION ======================

@app.post("/encrypt/shuffle")
async def encrypt_shuffle(image: UploadFile = File(...), key: int = Form(...)):
    img_bytes = await image.read()

    encrypted_img = encrypt_image_shuffle(img_bytes, key)

    return StreamingResponse(io.BytesIO(encrypted_img),
                             media_type="image/png",
                             headers={"Content-Disposition": "attachment; filename=shuffled.png"})


@app.post("/decrypt/shuffle")
async def decrypt_shuffle(image: UploadFile = File(...), key: int = Form(...)):
    img_bytes = await image.read()

    decrypted_img = decrypt_image_shuffle(img_bytes, key)

    return StreamingResponse(io.BytesIO(decrypted_img),
                             media_type="image/png",
                             headers={"Content-Disposition": "attachment; filename=unshuffled.png"})


# ========================= STEGANOGRAPHY ============================

@app.post("/stego/hide")
async def hide(image: UploadFile = File(...), message: str = Form(...)):
    img_bytes = await image.read()

    stego_image = hide_message_in_image(img_bytes, message)

    return StreamingResponse(io.BytesIO(stego_image),
                             media_type="image/png",
                             headers={"Content-Disposition": "attachment; filename=stego.png"})


@app.post("/stego/extract")
async def extract(image: UploadFile = File(...)):
    img_bytes = await image.read()

    msg = extract_message(img_bytes)
    return JSONResponse({"hidden_message": msg})


# ========================= HASH CHECK ===============================

@app.post("/hash")
async def hash_file(file: UploadFile = File(...)):
    data = await file.read()
    return {"sha256_hash": generate_sha256(data)}

@app.post("/encrypt/aes-gcm")
async def aes_gcm_encrypt(file: UploadFile = File(...), password: str = Form(...)):
    data = await file.read()
    encrypted = encrypt_aes_gcm(data, password)
    return StreamingResponse(io.BytesIO(encrypted),
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=aesgcm.bin"})
    

@app.post("/decrypt/aes-gcm")
async def aes_gcm_decrypt(file: UploadFile = File(...), password: str = Form(...)):
    data = await file.read()
    try:
        decrypted = decrypt_aes_gcm(data, password)
        return StreamingResponse(io.BytesIO(decrypted),
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=recovered.png"})
    except:
        return JSONResponse({"error": "Integrity Failed / Wrong Password"}, status_code=400)


@app.get("/signature/generate-keys")
async def gen_keys():
    private, public = generate_rsa_keys()
    return {
        "private_key": private.decode(),
        "public_key": public.decode()
    }


@app.post("/signature/sign")
async def sign_image(file: UploadFile = File(...), private_key: str = Form(...)):
    data = await file.read()
    sig = sign_data(data, private_key.encode())
    return StreamingResponse(io.BytesIO(sig),
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=signature.sig"})

@app.post("/signature/verify")
async def verify_image_signature(
    file: UploadFile = File(...),
    signature_file: UploadFile = File(...),
    public_key: str = Form(...)
):
    data = await file.read()
    sign = await signature_file.read()

    status = verify_signature(data, sign, public_key.encode())
    return {"verified": status}


@app.post("/watermark")
async def watermark(image: UploadFile = File(...), text: str = Form(...)):
    img = await image.read()
    output = add_watermark(img, text)

    return StreamingResponse(io.BytesIO(output),
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=watermarked.png"})

@app.post("/attack/tamper")
async def tamper(file: UploadFile = File(...)):
    data = await file.read()
    tampered = tamper_data(data)

    o, m = compare_hash(data, tampered)

    return {
        "original_hash": o,
        "tampered_hash": m,
        "message": "Tampering changes integrity"
    }
