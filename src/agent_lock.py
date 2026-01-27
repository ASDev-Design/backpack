"""
Agent lock file management.

This module provides the AgentLock class for creating, reading, and updating
encrypted agent.lock files that contain credentials, personality, and memory.
"""

import json
import os
from typing import Dict, Any, Optional
from .crypto import encrypt_data, decrypt_data

class AgentLock:
    """
    Manages encrypted agent.lock files containing agent configuration and state.
    
    The agent.lock file contains three encrypted layers:
    1. Credentials: Placeholders for required API keys
    2. Personality: System prompts and agent configuration
    3. Memory: Ephemeral agent state
    
    All data is encrypted using a master key (from AGENT_MASTER_KEY env var).
    """
    def __init__(self, file_path: str = "agent.lock"):
        """
        Initialize an AgentLock instance.
        
        Args:
            file_path: Path to the agent.lock file (default: "agent.lock")
        """
        self.file_path = file_path
        self.master_key = os.environ.get("AGENT_MASTER_KEY", "default-key")
    
    def create(self, credentials: Dict[str, str], personality: Dict[str, str], memory: Dict[str, Any] = None) -> None:
        """
        Create a new agent.lock file with encrypted layers.
        
        Args:
            credentials: Dictionary mapping credential names to placeholder values
            personality: Dictionary containing system prompts and configuration
            memory: Optional dictionary for ephemeral agent state (default: empty dict)
        """
        if memory is None:
            memory = {}
        
        data = {
            "version": "1.0",
            "layers": {
                "credentials": encrypt_data(json.dumps(credentials), self.master_key),
                "personality": encrypt_data(json.dumps(personality), self.master_key),
                "memory": encrypt_data(json.dumps(memory), self.master_key)
            }
        }
        
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def read(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        Read and decrypt the agent.lock file.
        
        Returns:
            A dictionary with keys 'credentials', 'personality', and 'memory',
            each containing the decrypted data. Returns None if the file doesn't
            exist or decryption fails.
        """
        if not os.path.exists(self.file_path):
            return None
        
        with open(self.file_path, 'r') as f:
            data = json.load(f)
        
        try:
            return {
                "credentials": json.loads(decrypt_data(data["layers"]["credentials"], self.master_key)),
                "personality": json.loads(decrypt_data(data["layers"]["personality"], self.master_key)),
                "memory": json.loads(decrypt_data(data["layers"]["memory"], self.master_key))
            }
        except Exception:
            return None
    
    def update_memory(self, memory: Dict[str, Any]) -> None:
        """
        Update the memory layer of the agent.lock file.
        
        This preserves existing credentials and personality while updating
        only the ephemeral memory state.
        
        Args:
            memory: New memory dictionary to store
        """
        agent_data = self.read()
        if agent_data:
            agent_data["memory"] = memory
            self.create(agent_data["credentials"], agent_data["personality"], memory)
    
    def get_required_keys(self) -> list:
        """
        Get a list of required credential keys from the agent.lock file.
        
        Returns:
            A list of credential key names (e.g., ['OPENAI_API_KEY', 'TWITTER_TOKEN'])
        """
        agent_data = self.read()
        if agent_data and "credentials" in agent_data:
            return list(agent_data["credentials"].keys())
        return []