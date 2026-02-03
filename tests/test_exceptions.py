"""
Tests for custom exception classes.
"""

from backpack.exceptions import (
    AgentLockError,
    AgentLockNotFoundError,
    BackpackError,
    CryptoError,
    DecryptionError,
    EncryptionError,
    InvalidPasswordError,
    KeychainError,
    KeyNotFoundError,
    ValidationError,
)


class TestBackpackError:
    """Tests for base BackpackError class."""
    
    def test_backpack_error_basic(self):
        """Test basic BackpackError creation."""
        error = BackpackError("Test error")
        
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details is None
    
    def test_backpack_error_with_details(self):
        """Test BackpackError with details."""
        error = BackpackError("Test error", "Additional details")
        
        assert "Test error" in str(error)
        assert "Additional details" in str(error)
        assert error.details == "Additional details"


class TestCryptoErrors:
    """Tests for cryptographic exception classes."""
    
    def test_crypto_error_inheritance(self):
        """Test that CryptoError inherits from BackpackError."""
        error = CryptoError("Crypto error")
        
        assert isinstance(error, BackpackError)
        assert isinstance(error, CryptoError)
    
    def test_decryption_error_default(self):
        """Test DecryptionError with default message."""
        error = DecryptionError()
        
        assert isinstance(error, CryptoError)
        assert "Decryption failed" in str(error)
    
    def test_decryption_error_custom(self):
        """Test DecryptionError with custom message."""
        error = DecryptionError("Custom decryption error", "Custom details")
        
        assert "Custom decryption error" in str(error)
        assert "Custom details" in str(error)
    
    def test_encryption_error_default(self):
        """Test EncryptionError with default message."""
        error = EncryptionError()
        
        assert isinstance(error, CryptoError)
        assert "Encryption failed" in str(error)


class TestKeychainErrors:
    """Tests for keychain exception classes."""
    
    def test_keychain_error_inheritance(self):
        """Test that KeychainError inherits from BackpackError."""
        error = KeychainError("Keychain error")
        
        assert isinstance(error, BackpackError)
        assert isinstance(error, KeychainError)
    
    def test_key_not_found_error(self):
        """Test KeyNotFoundError."""
        error = KeyNotFoundError("TEST_KEY")
        
        assert isinstance(error, KeychainError)
        assert "TEST_KEY" in str(error)
        assert error.key_name == "TEST_KEY"
        assert "backpack key add" in str(error).lower()


class TestAgentLockErrors:
    """Tests for agent lock exception classes."""
    
    def test_agent_lock_error_inheritance(self):
        """Test that AgentLockError inherits from BackpackError."""
        error = AgentLockError("Lock error")
        
        assert isinstance(error, BackpackError)
        assert isinstance(error, AgentLockError)
    
    def test_agent_lock_not_found_error_default(self):
        """Test AgentLockNotFoundError with default path."""
        error = AgentLockNotFoundError()
        
        assert isinstance(error, AgentLockError)
        assert "agent.lock" in str(error)
        assert error.file_path == "agent.lock"
        assert "backpack init" in str(error).lower()
    
    def test_agent_lock_not_found_error_custom(self):
        """Test AgentLockNotFoundError with custom path."""
        error = AgentLockNotFoundError("custom.lock")
        
        assert "custom.lock" in str(error)
        assert error.file_path == "custom.lock"


class TestValidationErrors:
    """Tests for validation exception classes."""
    
    def test_validation_error_inheritance(self):
        """Test that ValidationError inherits from BackpackError."""
        error = ValidationError("Validation error")
        
        assert isinstance(error, BackpackError)
        assert isinstance(error, ValidationError)
    
    def test_invalid_password_error_default(self):
        """Test InvalidPasswordError with default message."""
        error = InvalidPasswordError()
        
        assert isinstance(error, ValidationError)
        assert "Invalid password" in str(error)
    
    def test_invalid_password_error_custom(self):
        """Test InvalidPasswordError with custom reason."""
        error = InvalidPasswordError("Password too short")
        
        assert "Password too short" in str(error)
