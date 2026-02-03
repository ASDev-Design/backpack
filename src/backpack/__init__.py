"""
Backpack Agent Container System.

This package provides the CLI and primitives for managing encrypted agent
containers (`agent.lock`), secure key storage, and just-in-time injection.
"""

__version__ = "0.1.3"

# Export exceptions for easy importing
from .exceptions import (  # noqa: F401
    AgentLockCorruptedError,
    AgentLockError,
    AgentLockNotFoundError,
    AgentLockReadError,
    AgentLockWriteError,
    BackpackError,
    CryptoError,
    DecryptionError,
    EncryptionError,
    InvalidKeyNameError,
    InvalidPasswordError,
    InvalidPathError,
    KeychainAccessError,
    KeychainDeletionError,
    KeychainError,
    KeychainStorageError,
    KeyDerivationError,
    KeyNotFoundError,
    ScriptExecutionError,
    ValidationError,
)

__all__ = [
    "BackpackError",
    "CryptoError",
    "DecryptionError",
    "EncryptionError",
    "KeyDerivationError",
    "KeychainError",
    "KeyNotFoundError",
    "KeychainAccessError",
    "KeychainStorageError",
    "KeychainDeletionError",
    "AgentLockError",
    "AgentLockNotFoundError",
    "AgentLockCorruptedError",
    "AgentLockReadError",
    "AgentLockWriteError",
    "ValidationError",
    "InvalidPathError",
    "InvalidKeyNameError",
    "InvalidPasswordError",
    "ScriptExecutionError",
]

