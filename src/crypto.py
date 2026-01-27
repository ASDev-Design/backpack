"""
Cryptographic utilities for encrypting and decrypting agent data.

This module provides functions for deriving encryption keys from passwords
using PBKDF2 and encrypting/decrypting data using Fernet symmetric encryption.
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

def derive_key(password: str, salt: bytes = None) -> bytes:
    """
    Derive an encryption key from a password using PBKDF2.
    
    Args:
        password: The password to derive the key from
        salt: Optional salt bytes. If None, a random salt is generated.
    
    Returns:
        A tuple of (key, salt) where key is a base64-encoded Fernet key
        and salt is the salt bytes used (or generated).
    """
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_data(data: str, password: str) -> dict:
    """
    Encrypt a string using PBKDF2 key derivation and Fernet encryption.
    
    Args:
        data: The plaintext string to encrypt
        password: The password to use for key derivation
    
    Returns:
        A dictionary containing:
        - 'data': Base64-encoded encrypted data
        - 'salt': Base64-encoded salt used for key derivation
    """
    key, salt = derive_key(password)
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return {
        'data': base64.b64encode(encrypted).decode(),
        'salt': base64.b64encode(salt).decode()
    }

def decrypt_data(encrypted_dict: dict, password: str) -> str:
    """
    Decrypt data that was encrypted with encrypt_data().
    
    Args:
        encrypted_dict: A dictionary containing:
            - 'data': Base64-encoded encrypted data
            - 'salt': Base64-encoded salt used for key derivation
        password: The password used for encryption
    
    Returns:
        The decrypted plaintext string
    
    Raises:
        Exception: If decryption fails (wrong password, corrupted data, etc.)
    """
    salt = base64.b64decode(encrypted_dict['salt'])
    key, _ = derive_key(password, salt)
    f = Fernet(key)
    encrypted_data = base64.b64decode(encrypted_dict['data'])
    return f.decrypt(encrypted_data).decode()