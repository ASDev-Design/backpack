"""
OS keychain integration for secure credential storage.

This module provides functions for storing, retrieving, and managing
API keys and other credentials using the platform's native keyring service.
"""

import keyring
import json
from typing import Dict, Optional

SERVICE_NAME = "backpack-agent"

def store_key(key_name: str, key_value: str) -> None:
    """
    Store a key-value pair in the OS keychain.
    
    Args:
        key_name: The name/identifier of the key
        key_value: The secret value to store
    """
    keyring.set_password(SERVICE_NAME, key_name, key_value)

def get_key(key_name: str) -> Optional[str]:
    """
    Retrieve a key value from the OS keychain.
    
    Args:
        key_name: The name/identifier of the key to retrieve
    
    Returns:
        The stored key value, or None if not found
    """
    return keyring.get_password(SERVICE_NAME, key_name)

def list_keys() -> Dict[str, bool]:
    """
    List all keys registered in the keychain.
    
    Note: The OS keyring doesn't provide native list functionality,
    so we maintain a registry of keys.
    
    Returns:
        A dictionary mapping key names to True (indicating they exist)
    """
    # Note: keyring doesn't provide list functionality, so we maintain a registry
    registry = get_key("_registry")
    if registry:
        return json.loads(registry)
    return {}

def register_key(key_name: str) -> None:
    """
    Register a key name in the keychain registry.
    
    This is used to track which keys exist, since the OS keyring
    doesn't provide native list functionality.
    
    Args:
        key_name: The name of the key to register
    """
    registry = list_keys()
    registry[key_name] = True
    keyring.set_password(SERVICE_NAME, "_registry", json.dumps(registry))

def delete_key(key_name: str) -> None:
    """
    Delete a key from the keychain and registry.
    
    Args:
        key_name: The name of the key to delete
    
    Raises:
        Exception: If the key doesn't exist or deletion fails
    """
    keyring.delete_password(SERVICE_NAME, key_name)
    registry = list_keys()
    registry.pop(key_name, None)
    keyring.set_password(SERVICE_NAME, "_registry", json.dumps(registry))