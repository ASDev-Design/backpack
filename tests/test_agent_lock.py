"""
Tests for agent_lock module - agent lock file management.
"""

import json
import os
from unittest.mock import patch

import pytest

from backpack.agent_lock import AgentLock


@pytest.fixture(autouse=True)
def mock_audit_logger():
    """Mock the audit logger to prevent file writes and verify calls."""
    with patch("backpack.agent_lock.AuditLogger") as mock_cls:
        yield mock_cls.return_value


class TestAgentLockInit:
    """Tests for AgentLock initialization."""
    
    def test_init_default_path(self):
        """Test initialization with default path."""
        agent_lock = AgentLock()
        
        assert agent_lock.file_path == "agent.lock"
        assert agent_lock.master_key is not None
    
    def test_init_custom_path(self, temp_dir):
        """Test initialization with custom path."""
        custom_path = os.path.join(temp_dir, "custom.lock")
        agent_lock = AgentLock(custom_path)
        
        assert agent_lock.file_path == custom_path
    
    def test_init_master_key_from_env(self, clean_env, monkeypatch):
        """Test that master key is read from environment."""
        monkeypatch.setenv("AGENT_MASTER_KEY", "env-master-key")
        
        agent_lock = AgentLock()
        
        assert agent_lock.master_key == "env-master-key"
    
    def test_init_master_key_default(self, clean_env):
        """Test default master key when env var not set."""
        agent_lock = AgentLock()
        
        assert agent_lock.master_key == "default-key"


class TestAgentLockCreate:
    """Tests for creating agent.lock files."""
    
    def test_create_basic(self, test_agent_lock_path, test_master_key, 
                         sample_credentials, sample_personality, sample_memory, mock_audit_logger):
        """Test basic agent.lock file creation."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        agent_lock.create(sample_credentials, sample_personality, sample_memory)
        
        assert os.path.exists(test_agent_lock_path)
        
        with open(test_agent_lock_path, 'r') as f:
            data = json.load(f)
        
        assert "version" in data
        assert "layers" in data
        assert "credentials" in data["layers"]
        assert "personality" in data["layers"]
        assert "memory" in data["layers"]
        
        mock_audit_logger.log_event.assert_called_with("lock_created", {"path": test_agent_lock_path})
    
    def test_create_default_memory(self, test_agent_lock_path, test_master_key,
                                  sample_credentials, sample_personality):
        """Test creation with default empty memory."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        agent_lock.create(sample_credentials, sample_personality)
        
        # Read and verify memory is empty dict
        result = agent_lock.read()
        assert result is not None
        assert result["memory"] == {}

    def test_create_empty_credentials(self, test_agent_lock_path, test_master_key,
                                      sample_personality):
        """Test creation with empty credentials."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        agent_lock.create({}, sample_personality)

        result = agent_lock.read()
        assert result is not None
        assert result["credentials"] == {}

    def test_create_overwrite_existing(self, test_agent_lock_path, test_master_key,
                                      sample_credentials, sample_personality):
        """Test that create overwrites existing file."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        # Create first time
        agent_lock.create(sample_credentials, sample_personality)
        first_result = agent_lock.read()

        # Create again with different data
        new_personality = {"system_prompt": "Different prompt", "tone": "casual"}
        agent_lock.create(sample_credentials, new_personality)
        second_result = agent_lock.read()

        assert first_result is not None
        assert second_result is not None
        assert first_result["personality"] != second_result["personality"]
        assert second_result["personality"]["system_prompt"] == "Different prompt"


class TestAgentLockRead:
    """Tests for reading agent.lock files."""
    
    def test_read_existing(self, test_agent_lock_path, test_master_key,
                          sample_credentials, sample_personality, sample_memory):
        """Test reading existing agent.lock file."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        agent_lock.create(sample_credentials, sample_personality, sample_memory)
        result = agent_lock.read()
        
        assert result is not None
        assert "credentials" in result
        assert "personality" in result
        assert "memory" in result
        assert result["credentials"] == sample_credentials
        assert result["personality"] == sample_personality
        assert result["memory"] == sample_memory
    
    def test_read_nonexistent(self, test_agent_lock_path, test_master_key):
        """Test reading non-existent file."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        result = agent_lock.read()
        
        assert result is None
    
    def test_read_wrong_master_key(self, test_agent_lock_path, test_master_key,
                                  sample_credentials, sample_personality):
        """Test reading with wrong master key."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        # Create with one key
        agent_lock.create(sample_credentials, sample_personality)
        
        # Try to read with different key
        agent_lock.master_key = "wrong-key"
        result = agent_lock.read()
        
        assert result is None
    
    def test_read_corrupted_file(self, test_agent_lock_path, test_master_key):
        """Test reading corrupted agent.lock file."""
        # Create invalid JSON file
        with open(test_agent_lock_path, 'w') as f:
            f.write("invalid json content!!!")
        
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        # Should return None for corrupted files (current implementation)
        result = agent_lock.read()
        assert result is None


class TestAgentLockUpdateMemory:
    """Tests for updating memory layer."""
    
    def test_update_memory_basic(self, test_agent_lock_path, test_master_key,
                                 sample_credentials, sample_personality, sample_memory):
        """Test basic memory update."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        # Create initial lock
        agent_lock.create(sample_credentials, sample_personality, sample_memory)
        
        # Update memory
        new_memory = {"user_id": "new_user", "session_count": 5}
        agent_lock.update_memory(new_memory)
        
        # Verify update
        result = agent_lock.read()
        assert result["memory"] == new_memory
        assert result["credentials"] == sample_credentials  # Should be preserved
        assert result["personality"] == sample_personality  # Should be preserved
    
    def test_update_memory_preserves_other_layers(self, test_agent_lock_path, test_master_key,
                                                   sample_credentials, sample_personality):
        """Test that memory update preserves credentials and personality."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        # Create initial lock
        agent_lock.create(sample_credentials, sample_personality)
        original = agent_lock.read()
        
        # Update memory
        new_memory = {"test": "data"}
        agent_lock.update_memory(new_memory)
        
        # Verify other layers unchanged
        updated = agent_lock.read()
        assert updated["credentials"] == original["credentials"]
        assert updated["personality"] == original["personality"]
        assert updated["memory"] == new_memory


class TestAgentLockGetRequiredKeys:
    """Tests for getting required keys."""
    
    def test_get_required_keys_basic(self, test_agent_lock_path, test_master_key,
                                     sample_credentials, sample_personality):
        """Test getting required keys from agent.lock."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        agent_lock.create(sample_credentials, sample_personality)
        
        required_keys = agent_lock.get_required_keys()
        
        assert isinstance(required_keys, list)
        assert len(required_keys) == len(sample_credentials)
        assert "OPENAI_API_KEY" in required_keys
        assert "TWITTER_TOKEN" in required_keys
    
    def test_get_required_keys_empty(self, test_agent_lock_path, test_master_key,
                                     sample_personality):
        """Test getting required keys when credentials are empty."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        agent_lock.create({}, sample_personality)
        
        required_keys = agent_lock.get_required_keys()
        
        assert required_keys == []
    
    def test_get_required_keys_nonexistent_file(self, test_agent_lock_path, test_master_key):
        """Test getting required keys when file doesn't exist."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        required_keys = agent_lock.get_required_keys()
        
        assert required_keys == []


class TestAgentLockIntegration:
    """Integration tests for AgentLock operations."""
    
    def test_full_workflow(self, test_agent_lock_path, test_master_key,
                          sample_credentials, sample_personality, sample_memory):
        """Test complete workflow: create, read, update, get keys."""
        agent_lock = AgentLock(test_agent_lock_path)
        agent_lock.master_key = test_master_key
        
        # Create
        agent_lock.create(sample_credentials, sample_personality, sample_memory)
        
        # Read
        result = agent_lock.read()
        assert result is not None
        
        # Get required keys
        keys = agent_lock.get_required_keys()
        assert len(keys) == 2
        
        # Update memory
        new_memory = {"updated": True}
        agent_lock.update_memory(new_memory)
        
        # Verify update
        updated = agent_lock.read()
        assert updated["memory"] == new_memory
    
    def test_multiple_agents_different_paths(self, temp_dir, test_master_key,
                                            sample_credentials, sample_personality):
        """Test managing multiple agent.lock files."""
        path1 = os.path.join(temp_dir, "agent1.lock")
        path2 = os.path.join(temp_dir, "agent2.lock")
        
        agent1 = AgentLock(path1)
        agent1.master_key = test_master_key
        agent1.create(sample_credentials, {"system_prompt": "Agent 1"})
        
        agent2 = AgentLock(path2)
        agent2.master_key = test_master_key
        agent2.create(sample_credentials, {"system_prompt": "Agent 2"})
        
        # Verify they're independent
        result1 = agent1.read()
        result2 = agent2.read()

        assert result1 is not None
        assert result2 is not None
        assert result1["personality"]["system_prompt"] == "Agent 1"
        assert result2["personality"]["system_prompt"] == "Agent 2"
