# Agent Lock

The `backpack.agent_lock` module provides the `AgentLock` class for managing encrypted `agent.lock` files. These files contain credentials, personality, and memory for an agent.

## Class: AgentLock

Manages encrypted agent.lock files.

### `__init__(file_path: str = "agent.lock", master_key: str = None)`

Initialize an AgentLock instance.

- **file_path**: Path to the agent.lock file (default: "agent.lock")
- **master_key**: Optional master key to use (overrides `AGENT_MASTER_KEY` env var)

### `create(credentials: Dict[str, str], personality: Dict[str, str], memory: Dict[str, Any] = None) -> None`

Create a new agent.lock file with encrypted layers.

- **credentials**: Dictionary mapping credential names to placeholder values.
- **personality**: Dictionary containing system prompts and configuration.
- **memory**: Optional dictionary for ephemeral agent state (default: empty dict).

**Raises:**
- `ValidationError`: If input data is invalid.
- `EncryptionError`: If encryption fails.
- `AgentLockWriteError`: If writing the file fails.

### `read() -> Optional[Dict[str, Dict[str, Any]]]`

Read and decrypt the agent.lock file.

**Returns:**
A dictionary with keys `'credentials'`, `'personality'`, and `'memory'`, each containing the decrypted data. Returns `None` if the file doesn't exist or decryption fails.

**Raises:**
- `AgentLockReadError`: If reading the file fails (I/O/permissions).
- `InvalidPathError`: If the path exists but is not a file.

### `update_memory(memory: Dict[str, Any]) -> None`

Update the memory layer of the agent.lock file. Preserves existing credentials and personality.

- **memory**: New memory dictionary to store.

**Raises:**
- `AgentLockNotFoundError`: If agent.lock file doesn't exist.
- `ValidationError`: If memory is not a dictionary.
- `AgentLockWriteError`: If writing the updated file fails.

### `get_required_keys() -> list`

Get a list of required credential keys from the agent.lock file.

**Returns:**
A list of credential key names (e.g., `['OPENAI_API_KEY', 'TWITTER_TOKEN']`).
