# Cryptography Utilities

The `backpack.crypto` module provides functions for encrypting and decrypting agent data using Fernet symmetric encryption and PBKDF2 key derivation.

## Functions

### `derive_key(password: str, salt: bytes = None) -> bytes`

Derive an encryption key from a password using PBKDF2.

- **password**: The password to derive the key from.
- **salt**: Optional salt bytes. If `None`, a random salt is generated.

**Returns:**
A tuple of `(key, salt)` where key is a base64-encoded Fernet key and salt is the salt bytes used.

**Raises:**
- `InvalidPasswordError`: If password is empty or None.
- `KeyDerivationError`: If key derivation fails.

### `encrypt_data(data: str, password: str) -> dict`

Encrypt a string using PBKDF2 key derivation and Fernet encryption.

- **data**: The plaintext string to encrypt.
- **password**: The password to use for key derivation.

**Returns:**
A dictionary containing:
- `'data'`: Base64-encoded encrypted data.
- `'salt'`: Base64-encoded salt used for key derivation.

**Raises:**
- `ValidationError`: If data is not a string or is None.
- `EncryptionError`: If encryption fails.

### `decrypt_data(encrypted_dict: dict, password: str) -> str`

Decrypt data that was encrypted with `encrypt_data()`.

- **encrypted_dict**: A dictionary containing `'data'` and `'salt'`.
- **password**: The password used for encryption.

**Returns:**
The decrypted plaintext string.

**Raises:**
- `ValidationError`: If encrypted_dict is invalid.
- `DecryptionError`: If decryption fails.
