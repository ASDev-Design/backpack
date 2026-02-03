"""
Tests for keychain module - OS keychain integration.
"""

import json
from unittest.mock import patch

import pytest

from backpack.keychain import SERVICE_NAME, delete_key, get_key, list_keys, register_key, store_key


@pytest.fixture(autouse=True)
def mock_audit_logger():
    """Mock the audit logger to prevent file writes and verify calls."""
    with patch("backpack.keychain.audit_logger") as mock:
        yield mock


class TestStoreKey:
    """Tests for storing keys in keychain."""
    
    def test_store_key_basic(self, mock_keyring, mock_audit_logger):
        """Test basic key storage."""
        store_key("TEST_KEY", "test-value-123")
        
        assert mock_keyring[(SERVICE_NAME, "TEST_KEY")] == "test-value-123"
        mock_audit_logger.log_event.assert_called_with(
            "store_key", 
            {"service": SERVICE_NAME, "key_name": "TEST_KEY"}
        )
    
    def test_store_key_overwrite(self, mock_keyring):
        """Test overwriting existing key."""
        store_key("TEST_KEY", "value1")
        assert mock_keyring[(SERVICE_NAME, "TEST_KEY")] == "value1"
        
        store_key("TEST_KEY", "value2")
        assert mock_keyring[(SERVICE_NAME, "TEST_KEY")] == "value2"
    
    def test_store_key_special_characters(self, mock_keyring):
        """Test storing key with special characters."""
        value = "test!@#$%^&*()_+-=[]{}|;':\",./<>?"
        store_key("SPECIAL_KEY", value)
        
        assert mock_keyring[(SERVICE_NAME, "SPECIAL_KEY")] == value
    
    def test_store_key_unicode(self, mock_keyring):
        """Test storing key with unicode characters."""
        value = "测试值 🚀"
        store_key("UNICODE_KEY", value)
        
        assert mock_keyring[(SERVICE_NAME, "UNICODE_KEY")] == value


class TestGetKey:
    """Tests for retrieving keys from keychain."""
    
    def test_get_key_existing(self, mock_keyring):
        """Test retrieving existing key."""
        mock_keyring[(SERVICE_NAME, "TEST_KEY")] = "test-value"
        
        result = get_key("TEST_KEY")
        
        assert result == "test-value"
    
    def test_get_key_nonexistent(self, mock_keyring):
        """Test retrieving non-existent key."""
        result = get_key("NONEXISTENT_KEY")
        
        assert result is None
    
    def test_get_key_empty_string(self, mock_keyring):
        """Test retrieving key with empty value."""
        mock_keyring[(SERVICE_NAME, "EMPTY_KEY")] = ""
        
        result = get_key("EMPTY_KEY")
        
        assert result == ""


class TestListKeys:
    """Tests for listing keys in registry."""
    
    def test_list_keys_empty(self, mock_keyring):
        """Test listing keys when registry is empty."""
        result = list_keys()
        
        assert result == {}
    
    def test_list_keys_single(self, mock_keyring):
        """Test listing keys with one key."""
        register_key("KEY1")
        
        result = list_keys()
        
        assert "KEY1" in result
        assert result["KEY1"] is True
    
    def test_list_keys_multiple(self, mock_keyring):
        """Test listing keys with multiple keys."""
        register_key("KEY1")
        register_key("KEY2")
        register_key("KEY3")
        
        result = list_keys()
        
        assert len(result) == 3
        assert "KEY1" in result
        assert "KEY2" in result
        assert "KEY3" in result
        assert all(result.values())  # All should be True


class TestRegisterKey:
    """Tests for registering keys in registry."""
    
    def test_register_key_new(self, mock_keyring):
        """Test registering a new key."""
        register_key("NEW_KEY")
        
        result = list_keys()
        assert "NEW_KEY" in result
        assert result["NEW_KEY"] is True
    
    def test_register_key_existing(self, mock_keyring):
        """Test registering an existing key (should update)."""
        register_key("EXISTING_KEY")
        register_key("EXISTING_KEY")  # Register again
        
        result = list_keys()
        assert "EXISTING_KEY" in result
        assert result["EXISTING_KEY"] is True
    
    def test_register_key_multiple(self, mock_keyring):
        """Test registering multiple keys."""
        register_key("KEY1")
        register_key("KEY2")
        register_key("KEY3")
        
        result = list_keys()
        assert len(result) == 3


class TestDeleteKey:
    """Tests for deleting keys from keychain."""
    
    def test_delete_key_existing(self, mock_keyring):
        """Test deleting an existing key."""
        store_key("TO_DELETE", "value")
        register_key("TO_DELETE")
        
        delete_key("TO_DELETE")
        
        assert (SERVICE_NAME, "TO_DELETE") not in mock_keyring
        result = list_keys()
        assert "TO_DELETE" not in result
    
    def test_delete_key_nonexistent(self, mock_keyring):
        """Test deleting a non-existent key."""
        # Should not raise an exception
        try:
            delete_key("NONEXISTENT")
        except Exception as e:
            pytest.fail(f"delete_key raised exception: {e}")
    
    def test_delete_key_from_registry_only(self, mock_keyring):
        """Test deleting key that exists in registry but not keychain."""
        # Manually add to registry
        registry = {"REGISTRY_ONLY": True}
        mock_keyring[(SERVICE_NAME, "_registry")] = json.dumps(registry)
        
        delete_key("REGISTRY_ONLY")
        
        result = list_keys()
        assert "REGISTRY_ONLY" not in result


class TestKeychainIntegration:
    """Integration tests for keychain operations."""
    
    def test_full_workflow(self, mock_keyring):
        """Test complete workflow: store, get, list, delete."""
        # Store keys
        store_key("KEY1", "value1")
        register_key("KEY1")
        store_key("KEY2", "value2")
        register_key("KEY2")
        
        # List keys
        keys = list_keys()
        assert len(keys) == 2
        assert "KEY1" in keys
        assert "KEY2" in keys
        
        # Get keys
        assert get_key("KEY1") == "value1"
        assert get_key("KEY2") == "value2"
        
        # Delete one key
        delete_key("KEY1")
        
        # Verify deletion
        assert get_key("KEY1") is None
        keys = list_keys()
        assert "KEY1" not in keys
        assert "KEY2" in keys
    
    def test_registry_persistence(self, mock_keyring):
        """Test that registry persists across operations."""
        register_key("PERSIST1")
        register_key("PERSIST2")
        
        # Simulate reading registry again
        keys1 = list_keys()
        
        register_key("PERSIST3")
        keys2 = list_keys()
        
        assert "PERSIST1" in keys1
        assert "PERSIST2" in keys1
        assert "PERSIST1" in keys2
        assert "PERSIST2" in keys2
        assert "PERSIST3" in keys2
    
    def test_service_name_consistency(self):
        """Test that SERVICE_NAME is consistent."""
        assert SERVICE_NAME == "backpack-agent"
        assert isinstance(SERVICE_NAME, str)
        assert len(SERVICE_NAME) > 0
