import streamlit as st
import requests
from PIL import Image
import io
import hashlib
import math
import numpy as np
import matplotlib.pyplot as plt

# ===================== CONFIGURATION =====================
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SecureVision Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== UI & STYLING =====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600&display=swap');

    /* Global Styles */
    .stApp {
        background-color: #0e1117;
        color: #e6edf3;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
    }

    h1 {
        font-weight: 700;
        color: #58a6ff; /* GitHub Blue / Cyber Blue */
    }
    
    h2 {
        font-size: 1.5rem;
        color: #7ee787; /* Success Green */
        margin-top: 1rem;
        border-bottom: 1px solid #30363d;
        padding-bottom: 0.5rem;
    }

    /* Custom Header */
    .main-header {
        text-align: center;
        padding: 3rem 0;
        margin-bottom: 2rem;
        background: radial-gradient(circle at center, rgba(31,111,235,0.1) 0%, rgba(14,17,23,0) 70%);
        border-bottom: 1px solid #30363d;
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(88, 166, 255, 0.4);
    }
    
    .main-header h4 {
        color: #8b949e;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.1rem;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #238636;
        color: white;
        border: 1px solid rgba(240,246,252,0.1);
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #2ea043;
        box-shadow: 0 0 15px rgba(46, 160, 67, 0.5);
        transform: scale(1.02);
        border-color: #2ea043;
    }

    div.stDownloadButton > button {
        background-color: #1f6feb;
        color: white;
        width: 100%;
        border-radius: 6px;
    }
    
    div.stDownloadButton > button:hover {
        background-color: #388bfd;
        box-shadow: 0 0 15px rgba(56, 139, 253, 0.5);
    }

    /* Input Fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea, .stNumberInput > div > div > input {
        background-color: #0d1117;
        color: #e6edf3;
        border: 1px solid #30363d;
        border-radius: 6px;
    }

    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 1px #58a6ff;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0d1117;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #30363d;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #8b949e;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #238636;
        color: white;
    }

    /* Info/Success Boxes */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 6px;
        border: 1px solid rgba(255,255,255,0.1);
    }

</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("""
<div class="main-header">
    <h1>🛡️ SecureVision</h1>
    <h4>Advanced Cryptography & Steganography Suite</h4>
</div>
""", unsafe_allow_html=True)

# ===================== MAIN LAYOUT =====================
# Using a more concise distinct tab structure
tabs = st.tabs([
    "🔐 AES Encryption",
    "🛡️ AES-GCM",
    "🔀 Shuffle Pixel",
    "🕵️ Steganography",
    "✍️ Digital Sig",
    "🖼️ Watermark",
    "💀 Attack Sim",
    "📊 Dashboard"
])

# Unpack tabs for easier reference
tab_aes, tab_aesgcm, tab_shuffle, tab_stego, tab_sig, tab_watermark, tab_attack, tab_dash = tabs

# ==================== AES ENCRYPTION ===========================
with tab_aes:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 🔒 Encrypt Image")
        st.info("Standard AES encryption.")
        
        aes_enc_img = st.file_uploader("Upload Image", type=["png","jpg","jpeg"], key="aes_enc_up")
        aes_enc_pwd = st.text_input("Encryption Password", type="password", key="aes_enc_pw")
        
        if st.button("Encrypt Now", key="aes_enc_go"):
            if aes_enc_img and aes_enc_pwd:
                with st.spinner("Encrypting data..."):
                    files = {"image": aes_enc_img}
                    data = {"password": aes_enc_pwd}
                    try:
                        res = requests.post(f"{BASE_URL}/encrypt/aes", files=files, data=data)
                        if res.status_code == 200:
                            st.success("Encryption Successful!")
                            st.download_button("Download Encrypted File (.bin)", 
                                             data=res.content, 
                                             file_name="encrypted_image.bin",
                                             mime="application/octet-stream")
                        else:
                            st.error(f"Error: {res.text}")
                    except Exception as e:
                        st.error(f"Connection failed: {e}")

    with col2:
        st.markdown("### 🔓 Decrypt Image")
        st.info("Recover original image.")
        
        aes_dec_file = st.file_uploader("Upload Encrypted File (.bin)", type=["bin"], key="aes_dec_up")
        aes_dec_pwd = st.text_input("Decryption Password", type="password", key="aes_dec_pw")
        
        if st.button("Decrypt Now", key="aes_dec_go"):
            if aes_dec_file and aes_dec_pwd:
                with st.spinner("Decrypting data..."):
                    files = {"file": aes_dec_file}
                    data = {"password": aes_dec_pwd}
                    try:
                        res = requests.post(f"{BASE_URL}/decrypt/aes", files=files, data=data)
                        if res.status_code == 200:
                            try:
                                # Validation: corrupted bytes won't open as image
                                img = Image.open(io.BytesIO(res.content))
                                st.success("Decryption Successful!")
                                st.image(img, caption="Recovered Image", width=400)
                                st.download_button("Download Recovered Image", 
                                                 data=res.content, 
                                                 file_name="decrypted_image.png",
                                                 mime="image/png")
                            except Exception:
                                st.error("Decryption failed. Incorrect password or corrupted file.")
                        else:
                            st.error(f"Server Error: {res.status_code}")
                    except requests.exceptions.RequestException:
                        st.error("Failed to connect to backend.")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}")

# ==================== AES-GCM ENCRYPTION ===========================
with tab_aesgcm:
    st.markdown("## 🔐 AES-GCM (High Security Mode)")
    st.markdown("AES-Galois Counter Mode provides both confidentiality and data integrity.")
    
    col_gcm_enc, col_gcm_dec = st.columns(2, gap="large")
    
    with col_gcm_enc:
        st.markdown("#### Encrypt (GCM)")
        gcm_file = st.file_uploader("Upload Image to Encrypt", type=["png","jpg","jpeg"], key="gcm_enc_up")
        gcm_pwd = st.text_input("Password", type="password", key="gcm_enc_pw")
        
        if st.button("Encrypt (AES-GCM)", key="gcm_enc_btn"):
            if gcm_file and gcm_pwd:
                with st.spinner("Encrypting with AES-GCM..."):
                    files = {"file": gcm_file}
                    data = {"password": gcm_pwd}
                    try:
                        res = requests.post(f"{BASE_URL}/encrypt/aes-gcm", files=files, data=data)
                        if res.status_code == 200:
                            st.success("Secured Successfully!")
                            st.download_button("Download Secure File", data=res.content, file_name="secure_aesgcm.bin")
                        else:
                            st.error("Encryption failed")
                    except requests.exceptions.RequestException:
                        st.error("Failed to connect to backend.")
                        
    with col_gcm_dec:
        st.markdown("#### Decrypt (GCM)")
        gcm_dec_file = st.file_uploader("Upload AES-GCM File", type=["bin"], key="gcm_dec_up")
        gcm_dec_pwd = st.text_input("Password", type="password", key="gcm_dec_pw")
        
        if st.button("Decrypt (AES-GCM)", key="gcm_dec_btn"):
            if gcm_dec_file and gcm_dec_pwd:
                with st.spinner("Decrypting AES-GCM..."):
                    files = {"file": gcm_dec_file}
                    data = {"password": gcm_dec_pwd}
                    try:
                        res = requests.post(f"{BASE_URL}/decrypt/aes-gcm", files=files, data=data)
                        if res.status_code == 200:
                            st.success("Verified & Decrypted!")
                            st.image(res.content, caption="Recovered", width=300)
                            st.download_button("Download", data=res.content, file_name="recovered.png")
                        elif res.status_code == 400:
                             st.error("Integrity Check Failed! Wrong password or file tampered.")
                        else:
                            st.error(res.json().get("error", "Decryption Failed"))
                    except requests.exceptions.RequestException:
                        st.error("Failed to connect to backend.")

# ==================== SHUFFLE ENCRYPTION ===========================
with tab_shuffle:
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("### 🌀 Pixel Shuffle Encrypt")
        st.markdown("Reorders pixels using a chaotic map determined by a numeric key.")
        
        shuf_img = st.file_uploader("Upload Image", type=["png","jpg","jpeg"], key="shuf_enc_up")
        shuf_key = st.number_input("Security Key (Numeric)", step=1, min_value=1, key="shuf_enc_k")
        
        if st.button("Shuffle Image", key="shuf_enc_go"):
            if shuf_img:
                with st.spinner("Shuffling pixels..."):
                    files = {"image": shuf_img}
                    data = {"key": int(shuf_key)}
                    try:
                        res = requests.post(f"{BASE_URL}/encrypt/shuffle", files=files, data=data)
                        if res.status_code == 200:
                            st.success("Image Shuffled!")
                            st.image(res.content, caption="Shuffled Result", width=300)
                            st.download_button("Download Shuffled", data=res.content, file_name="shuffled.png", mime="image/png")
                        else:
                            st.error("Operation failed.")
                    except:
                        st.error("Backend offline.")

    with col2:
        st.markdown("### ↩️ Pixel Unshuffle")
        st.markdown("Restores the original image using the correct numeric key.")
        
        unshuf_img = st.file_uploader("Upload Shuffled Image", type=["png"], key="shuf_dec_up")
        unshuf_key = st.number_input("Security Key (Numeric)", step=1, min_value=1, key="shuf_dec_k")
        
        if st.button("Unshuffle Image", key="shuf_dec_go"):
            if unshuf_img:
                with st.spinner("Unshuffling..."):
                    files = {"image": unshuf_img}
                    data = {"key": int(unshuf_key)}
                    try:
                        res = requests.post(f"{BASE_URL}/decrypt/shuffle", files=files, data=data)
                        if res.status_code == 200:
                            try:
                                img = Image.open(io.BytesIO(res.content))
                                st.success("Image Restored!")
                                st.image(img, caption="Restored Image", width=300)
                                st.download_button("Download Restored", data=res.content, file_name="restored.png", mime="image/png")
                            except:
                                st.error("Decryption produced invalid image data. Check your key.")
                        else:
                            st.error("Failed. Key might be wrong.")
                    except:
                        st.error("Backend error.")

# ===================== STEGANOGRAPHY ===============================
with tab_stego:
    st.markdown("## 🕵️ Data Hiding (LSB Steganography)")
    st.markdown("Hide secret messages inside image pixels without noticeable visual changes.")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("#### Hide Message")
        stego_img = st.file_uploader("Cover Image", type=["png","jpg","jpeg"], key="steg_hide_up")
        stego_msg = st.text_area("Secret Message", placeholder="Enter confidential text here...")
        
        if st.button("Embed Message", key="steg_hide_go"):
            if stego_img and stego_msg:
                with st.spinner("Embedding message..."):
                    files = {"image": stego_img}
                    data = {"message": stego_msg}
                    res = requests.post(f"{BASE_URL}/stego/hide", files=files, data=data)
                    if res.status_code == 200:
                        st.success("Message Embedded Successfully!")
                        st.download_button("Download Stego Image", data=res.content, file_name="stego_image.png", mime="image/png")
                    else:
                        st.error("Failed to embed message.")
    
    with col2:
        st.markdown("#### Extract Message")
        stego_ext_img = st.file_uploader("Stego Image", type=["png"], key="steg_ext_up")
        
        if st.button("Extract Secret", key="steg_ext_go"):
            if stego_ext_img:
                with st.spinner("Scanning pixels..."):
                    files = {"image": stego_ext_img}
                    res = requests.post(f"{BASE_URL}/stego/extract", files=files)
                    if res.status_code == 200:
                        st.success("Message Found!")
                        st.code(res.json().get("hidden_message", "No content found"), language="text")
                    else:
                        st.error("No hidden message detected.")

# ===================== DIGITAL SIGNATURE ===============================
with tab_sig:
    st.markdown("## ✍️ Digital Signatures (RSA)")
    st.markdown("Verify file authenticity and integrity.")

    col_keys, col_sign, col_verify = st.columns(3, gap="medium")
    
    with col_keys:
        st.markdown("### 1. Key Generation")
        if st.button("Generate RSA Keypair"):
            res = requests.get(f"{BASE_URL}/signature/generate-keys")
            if res.status_code == 200:
                data = res.json()
                st.text_area("Private Key (Keep Safe)", data["private_key"], height=200)
                st.text_area("Public Key (Share)", data["public_key"], height=200)
                st.success("Keys Generated!")
    
    with col_sign:
        st.markdown("### 2. Sign Image")
        sign_img = st.file_uploader("Image to Sign", type=["png","jpg","jpeg"], key="sig_up")
        priv_key = st.text_area("Private Key", height=100, key="sig_pk")
        
        if st.button("create Signature"):
            if sign_img and priv_key:
                with st.spinner("Signing..."):
                    files = {"file": sign_img}
                    data = {"private_key": priv_key}
                    res = requests.post(f"{BASE_URL}/signature/sign", files=files, data=data)
                    if res.status_code == 200:
                        st.success("Signed!")
                        st.download_button("Download Signature (.sig)", data=res.content, file_name="image.sig")
    
    with col_verify:
        st.markdown("### 3. Verify Signature")
        ver_img = st.file_uploader("Original Image", type=["png","jpg","jpeg"], key="ver_up")
        ver_sig = st.file_uploader("Signature File (.sig)", type=["sig"], key="ver_sig_up")
        pub_key = st.text_area("Public Key", height=100, key="ver_pb")
        
        if st.button("Verify Authenticity"):
            if ver_img and ver_sig and pub_key:
                files = {"file": ver_img, "signature_file": ver_sig}
                data = {"public_key": pub_key}
                res = requests.post(f"{BASE_URL}/signature/verify", files=files, data=data)
                
                if res.status_code == 200:
                    valid = res.json().get("verified", False)
                    if valid:
                        st.success("✅ Signature VALID. Image is authentic.")
                    else:
                        st.error("❌ Signature INVALID. Image corrupted or key mismatch.")

# ===================== WATERMARK ===============================
with tab_watermark:
    st.markdown("## 🖊️ Watermarking")
    wm_col1, wm_col2 = st.columns([1, 2])
    
    with wm_col1:
        wm_img = st.file_uploader("Source Image", type=["png","jpg","jpeg"], key="wm_up")
        wm_text = st.text_input("Watermark Text", "CONFIDENTIAL")
        
        if st.button("Apply Watermark", key="wm_go"):
            if wm_img and wm_text:
                with st.spinner("Processing..."):
                    files = {"image": wm_img}
                    data = {"text": wm_text}
                    res = requests.post(f"{BASE_URL}/watermark", files=files, data=data)
                    if res.status_code == 200:
                        st.session_state['wm_result'] = res.content
                        st.success("Watermark applied.")
                    else:
                        st.error("Failed.")
                        
    with wm_col2:
        if 'wm_result' in st.session_state:
            st.image(st.session_state['wm_result'], caption="Watermarked Result", width=500)
            st.download_button("Download Image", data=st.session_state['wm_result'], file_name="watermarked.png", mime="image/png")

# ===================== ATTACK SIM ===============================
with tab_attack:
    st.markdown("## ⚔️ Tamper Simulation")
    st.warning("This tool simulates a 'Man-in-the-Middle' attack by modifying file bytes to test integrity checks.")
    
    atk_file = st.file_uploader("Upload File to Tamper", key="atk_up")
    
    if st.button("Execute Attack", type="primary"):
        if atk_file:
            files = {"file": atk_file}
            res = requests.post(f"{BASE_URL}/attack/tamper", files=files)
            if res.status_code == 200:
                data = res.json()
                col1, col2 = st.columns(2)
                col1.metric("Original Hash", f"{data['original_hash'][:16]}...")
                col2.metric("Tampered Hash", f"{data['tampered_hash'][:16]}...", delta="-Integrity Broken", delta_color="inverse")
                st.error("⚠️ File integrity has been compromised.")

# ===================== DASHBOARD ===============================
with tab_dash:
    st.markdown("## 📊 Security Dashboard")
    
    # Top metrics row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Encryption Standard", "AES-256")
    m2.metric("Key Derivation", "PBKDF2-HMAC")
    m3.metric("RSA Key Size", "2048-bit")
    m4.metric("System Status", "Secure 🟢")
    
    st.divider()
    
    # Check integrity section (previously Tab 5: Hash Checker)
    st.markdown("### 🧾 File Integrity Check (SHA-256)")
    col_hash_up, col_hash_res = st.columns([1, 2])
    
    with col_hash_up:
         hash_file = st.file_uploader("Upload file to Hash", key="hash_tool_up")
    with col_hash_res:
         if hash_file and st.button("Generate Hash", key="hash_tool_go"):
             with st.spinner("Calculating SHA-256..."):
                 files = {"file": hash_file}
                 try:
                     res = requests.post(f"{BASE_URL}/hash", files=files)
                     if res.status_code == 200:
                         st.code(res.json()["sha256_hash"], language="text")
                     else:
                         st.error("Error generating hash")
                 except:
                     st.error("Backend offline")
                     
    st.divider()
    
    col_upload, col_analysis = st.columns([1, 2])
    
    with col_upload:
        st.markdown("### File Forensics (Entropy)")
        dash_file = st.file_uploader("Analyze for Encryption/Randomness", key="dash_up")
        
    with col_analysis:
        if dash_file:
            byte_data = dash_file.read()
            
            # Entropy calculation
            probs = [byte_data.count(i)/len(byte_data) for i in set(byte_data)]
            entropy = -sum([p * math.log2(p) for p in probs])
            
            st.subheader(f"Entropy: {entropy:.4f} bits/byte")
            st.progress(min(entropy/8.0, 1.0))
            
            if entropy > 7.5:
                st.success("High Entropy: File is likely encrypted or compressed.")
            else:
                st.warning("Low Entropy: File likely contains plaintext or structure.")
            
            # Histogram
            try:
                img = Image.open(io.BytesIO(byte_data))
                st.markdown("#### Pixel Distribution (Histogram)")
                arr = np.array(img)
                fig, ax = plt.subplots(figsize=(10, 3))
                ax.hist(arr.ravel(), bins=256, color='cyan', alpha=0.7)
                ax.set_facecolor('#0e1117')
                fig.patch.set_facecolor('#0e1117')
                ax.tick_params(colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white') 
                st.pyplot(fig)
            except:
                st.info("Not an image file - skipping histogram.")
