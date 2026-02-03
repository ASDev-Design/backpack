# Keychain Integration

The `backpack.keychain` module provides functions for storing, retrieving, and managing API keys using the platform's native keyring service.

## Functions

### `store_key(key_name: str, key_value: str) -> None`

Store a key-value pair in the OS keychain.

- **key_name**: The name/identifier of the key.
- **key_value**: The secret value to store.

**Raises:**
- `InvalidKeyNameError`: If key_name is invalid.
- `KeychainStorageError`: If storing the key fails.

### `get_key(key_name: str) -> Optional[str]`

Retrieve a key value from the OS keychain.

- **key_name**: The name/identifier of the key.

**Returns:**
The stored key value, or `None` if not found.

**Raises:**
- `InvalidKeyNameError`: If key_name is invalid.
- `KeychainAccessError`: If accessing the keychain fails.

### `list_keys() -> Dict[str, bool]`

List all keys registered in the keychain.

**Returns:**
A dictionary mapping key names to `True`.

### `register_key(key_name: str) -> None`

Register a key name in the keychain registry. Used internally to track keys.

### `delete_key(key_name: str) -> None`

Delete a key from the keychain and registry.

- **key_name**: The name of the key to delete.

**Raises:**
- `InvalidKeyNameError`: If key_name is invalid.
- `KeychainDeletionError`: If deletion fails.
