
#crypt_utils.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from Crypto.Cipher import AES, DES3, Blowfish
from Crypto.Util.Padding import pad, unpad
import os

# Helper function for AES encryption
def aes_encrypt(data, key):
    iv = os.urandom(16)  # Generate a random IV for AES
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad data to be a multiple of 16 bytes for AES
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data  # Prepend IV to the ciphertext

# Helper function for 3DES encryption
def des3_encrypt(data, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    
    # Use PKCS7 padding instead of null bytes
    padded_data = pad(data, DES3.block_size)
    return cipher.encrypt(padded_data)

# Helper function for Blowfish encryption
def blowfish_encrypt(data, key):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    
    # Use PKCS7 padding for Blowfish
    padded_data = pad(data, Blowfish.block_size)
    return cipher.encrypt(padded_data)

# Hybrid encryption function (AES + 3DES + Blowfish)
def hybrid_encrypt(data):
    aes_key = os.urandom(32)  # 256-bit AES key
    des3_key = os.urandom(24)  # 192-bit 3DES key
    blowfish_key = os.urandom(16)  # 128-bit Blowfish key

    # Apply AES encryption
    aes_encrypted = aes_encrypt(data, aes_key)
    
    # Apply 3DES encryption on the AES-encrypted data
    des3_encrypted = des3_encrypt(aes_encrypted, des3_key)
    
    # Apply Blowfish encryption on the 3DES-encrypted data
    blowfish_encrypted = blowfish_encrypt(des3_encrypted, blowfish_key)

    return blowfish_encrypted, aes_key, des3_key, blowfish_key

# Decryption function (Reverse Order: Blowfish → 3DES → AES)
def decrypt_file(encrypted_data, aes_key, des3_key, blowfish_key):
    try:
        # Blowfish Decryption
        blowfish_cipher = Blowfish.new(blowfish_key, Blowfish.MODE_ECB)
        decrypted_data = blowfish_cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_data, Blowfish.block_size)

        # 3DES Decryption
        des3_cipher = DES3.new(des3_key, DES3.MODE_ECB)
        decrypted_data = des3_cipher.decrypt(decrypted_data)
        decrypted_data = unpad(decrypted_data, DES3.block_size)

        # AES Decryption (Extract IV)
        iv = decrypted_data[:16]  # First 16 bytes contain the IV
        encrypted_aes_data = decrypted_data[16:]  # Remaining data
        aes_cipher = AES.new(aes_key, AES.MODE_CBC, iv)  # Use the extracted IV
        decrypted_data = aes_cipher.decrypt(encrypted_aes_data)
        decrypted_data = unpad(decrypted_data, AES.block_size)

        return decrypted_data
    except Exception as e:
        print("Decryption error:", e)
        return None
