"""
Custom exception classes for Backpack Agent Container System.

This module defines specific exception types for different error scenarios,
providing better error handling and more informative error messages.
"""


from typing import Optional


class BackpackError(Exception):
    """Base exception class for all Backpack-related errors."""

    def __init__(self, message: str, details: Optional[str] = None):
        """
        Initialize a Backpack error.

        Args:
            message: Human-readable error message
            details: Optional additional details for debugging
        """
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        if self.details:
            return f"{self.message} (Details: {self.details})"
        return self.message


class CryptoError(BackpackError):
    """Exception raised for cryptographic operation errors."""


class DecryptionError(CryptoError):
    """Exception raised when decryption fails."""

    def __init__(self, message: str = "Decryption failed", details: Optional[str] = None):
        super().__init__(
            message
            or "Failed to decrypt data. This may be due to an incorrect password, corrupted data, or invalid format.",
            details,
        )


class EncryptionError(CryptoError):
    """Exception raised when encryption fails."""

    def __init__(self, message: str = "Encryption failed", details: Optional[str] = None):
        super().__init__(
            message or "Failed to encrypt data. Please check your input and try again.",
            details,
        )


class KeyDerivationError(CryptoError):
    """Exception raised when key derivation fails."""

    def __init__(self, message: str = "Key derivation failed", details: Optional[str] = None):
        super().__init__(
            message
            or "Failed to derive encryption key. This may indicate a problem with the password or salt.",
            details,
        )


class KeychainError(BackpackError):
    """Exception raised for keychain operation errors."""


class KeyNotFoundError(KeychainError):
    """Exception raised when a key is not found in the keychain."""

    def __init__(self, key_name: str):
        super().__init__(
            f"Key '{key_name}' not found in keychain",
            f"Use 'backpack key add {key_name}' to add this key to your vault",
        )
        self.key_name = key_name


class KeychainAccessError(KeychainError):
    """Exception raised when keychain access fails."""

    def __init__(self, message: str = "Failed to access keychain", details: Optional[str] = None):
        super().__init__(
            message
            or "Unable to access the OS keychain. Please check your system's keychain permissions.",
            details,
        )


class KeychainStorageError(KeychainError):
    """Exception raised when storing to keychain fails."""

    def __init__(self, key_name: str, details: Optional[str] = None):
        super().__init__(
            f"Failed to store key '{key_name}' in keychain",
            details or "Please check your system's keychain permissions and available storage",
        )
        self.key_name = key_name


class KeychainDeletionError(KeychainError):
    """Exception raised when deleting from keychain fails."""

    def __init__(self, key_name: str, details: Optional[str] = None):
        super().__init__(
            f"Failed to delete key '{key_name}' from keychain",
            details or "The key may not exist or keychain access may be denied",
        )
        self.key_name = key_name


class AgentLockError(BackpackError):
    """Exception raised for agent.lock file operation errors."""


class AgentLockNotFoundError(AgentLockError):
    """Exception raised when agent.lock file is not found."""

    def __init__(self, file_path: str = "agent.lock"):
        super().__init__(
            f"Agent lock file not found: {file_path}",
            "Run 'backpack init' to create an agent.lock file",
        )
        self.file_path = file_path


class AgentLockCorruptedError(AgentLockError):
    """Exception raised when agent.lock file is corrupted or invalid."""

    def __init__(self, file_path: str = "agent.lock", details: Optional[str] = None):
        super().__init__(
            f"Agent lock file is corrupted or invalid: {file_path}",
            details or "The file may have been modified or encrypted with a different key",
        )
        self.file_path = file_path


class AgentLockReadError(AgentLockError):
    """Exception raised when reading agent.lock file fails."""

    def __init__(self, file_path: str, details: Optional[str] = None):
        super().__init__(
            f"Failed to read agent lock file: {file_path}",
            details
            or "Please check file permissions and ensure the file is not locked by another process",
        )
        self.file_path = file_path


class AgentLockWriteError(AgentLockError):
    """Exception raised when writing agent.lock file fails."""

    def __init__(self, file_path: str, details: Optional[str] = None):
        super().__init__(
            f"Failed to write agent lock file: {file_path}",
            details or "Please check file permissions and available disk space",
        )
        self.file_path = file_path


class ValidationError(BackpackError):
    """Exception raised for input validation errors."""


class InvalidPathError(ValidationError):
    """Exception raised when a file path is invalid."""

    def __init__(self, path: str, reason: Optional[str] = None):
        super().__init__(
            f"Invalid path: {path}",
            reason or "The path does not exist or is not accessible",
        )
        self.path = path


class InvalidKeyNameError(ValidationError):
    """Exception raised when a key name is invalid."""

    def __init__(self, key_name: str, reason: Optional[str] = None):
        super().__init__(
            f"Invalid key name: {key_name}",
            reason
            or "Key names must be non-empty and contain only alphanumeric characters and underscores",
        )
        self.key_name = key_name


class InvalidPasswordError(ValidationError):
    """Exception raised when a password is invalid."""

    def __init__(self, reason: Optional[str] = None):
        super().__init__(
            "Invalid password",
            reason or "Password cannot be empty",
        )


class ScriptExecutionError(BackpackError):
    """Exception raised when agent script execution fails."""

    def __init__(self, script_path: str, details: Optional[str] = None):
        super().__init__(
            f"Failed to execute agent script: {script_path}",
            details or "Please check that the script exists and is executable",
        )
        self.script_path = script_path

