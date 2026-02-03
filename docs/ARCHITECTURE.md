# Architecture Documentation

## Overview

Backpack implements a secure, portable agent container system that encrypts and manages three distinct layers of agent data: credentials, personality, and memory.

## System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface                         │
│                  (src/cli.py)                            │
└──────────────┬──────────────────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼──────────┐
│ AgentLock   │  │   Keychain      │
│ Management  │  │   Integration   │
│(agent_lock) │  │  (keychain.py)  │
└──────┬──────┘  └─────────────────┘
       │
┌──────▼──────┐
│ Encryption  │
│  (crypto.py)│
└─────────────┘
```

### Data Flow

1. **Initialization Flow**
   ```
   User → CLI init → AgentLock.create()
   → Encrypt credentials, personality, memory
   → Write agent.lock file
   ```

2. **Execution Flow**
   ```
   User → CLI run → AgentLock.read()
   → Decrypt agent.lock
   → Get required keys → Keychain.get_key()
   → User consent prompt
   → Inject into environment
   → Execute agent script
   ```

3. **Key Management Flow**
   ```
   User → CLI key add → Keychain.store_key()
   → OS keyring storage
   → Registry update
   ```

## Three-Layer Encryption Model

### Layer 1: Credentials

**Purpose**: Store placeholders for required API keys and tokens

**Structure**:
```json
{
  "OPENAI_API_KEY": "placeholder_openai_api_key",
  "TWITTER_TOKEN": "placeholder_twitter_token"
}
```

**Encryption**: Encrypted as a JSON string using PBKDF2 + Fernet

**Usage**: When an agent runs, these placeholders are matched against keys in the user's keychain. If found, the actual values are injected into the environment.

### Layer 2: Personality

**Purpose**: Store agent configuration, system prompts, and behavioral parameters

**Structure**:
```json
{
  "system_prompt": "You are a senior financial analyst.",
  "tone": "formal",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**Encryption**: Encrypted as a JSON string using PBKDF2 + Fernet

**Usage**: Injected into environment variables (e.g., `AGENT_SYSTEM_PROMPT`, `AGENT_TONE`) for the agent to read.

### Layer 3: Memory

**Purpose**: Store ephemeral agent state that can be committed and shared

**Structure**:
```json
{
  "user_id": "user123",
  "session_history": [...],
  "last_tool_output": "...",
  "context": {...}
}
```

**Encryption**: Encrypted as a JSON string using PBKDF2 + Fernet

**Usage**: Can be updated during agent execution and persisted back to `agent.lock`. This enables stateful agents that can resume from checkpoints.

## Encryption Details

### Key Derivation

- **Algorithm**: PBKDF2-HMAC-SHA256
- **Iterations**: 100,000
- **Salt**: 16 random bytes (stored with encrypted data)
- **Key Length**: 32 bytes (Fernet-compatible)

### Encryption

- **Algorithm**: Fernet (symmetric authenticated encryption)
- **Encoding**: Base64 for storage
- **Master Key**: From `AGENT_MASTER_KEY` environment variable (default: "default-key")

### Security Properties

- **Confidentiality**: Data encrypted at rest
- **Integrity**: Fernet provides authenticated encryption
- **Key Management**: Master key should be set via environment variable
- **Salt**: Unique per encryption operation prevents rainbow table attacks

## Keychain Integration

### Platform Support

Backpack uses the `keyring` library which provides platform-native keychain access:

- **macOS**: Keychain Services
- **Linux**: Secret Service API (GNOME Keyring, KWallet)
- **Windows**: Windows Credential Manager

### Registry System

Since OS keyrings don't provide native list functionality, Backpack maintains a registry:

- Stored as `_registry` key in the keychain
- JSON format: `{"key_name": true, ...}`
- Updated on add/remove operations

## File Format: agent.lock

```json
{
  "version": "1.0",
  "layers": {
    "credentials": {
      "data": "base64_encrypted_credentials_json",
      "salt": "base64_salt"
    },
    "personality": {
      "data": "base64_encrypted_personality_json",
      "salt": "base64_salt"
    },
    "memory": {
      "data": "base64_encrypted_memory_json",
      "salt": "base64_salt"
    }
  }
}
```

## Design Decisions

### Why Three Separate Layers?

1. **Separation of Concerns**: Credentials, personality, and memory serve different purposes
2. **Selective Updates**: Can update memory without re-encrypting credentials
3. **Version Control**: Personality changes can be tracked in Git without exposing secrets
4. **Flexibility**: Different access patterns for different layers

### Why PBKDF2 + Fernet?

- **PBKDF2**: Industry-standard key derivation, resistant to brute force
- **Fernet**: Simple, secure, authenticated encryption with good Python support
- **Compatibility**: Works across platforms without additional dependencies

### Why OS Keychain?

- **Native Security**: Uses platform-provided secure storage
- **User Trust**: Users understand their OS keychain
- **No Additional Setup**: Works out of the box on all platforms
- **Integration**: Can leverage existing keychain management tools

## Future Enhancements

Potential improvements to consider:

1. **Key Rotation**: Support for rotating master keys
2. **Multi-User**: Shared keychains for team environments
3. **Key Derivation**: Per-layer keys for additional security
4. **Compression**: Compress data before encryption for large memory states
5. **Versioning**: Support for multiple agent.lock versions
6. **Remote Keychains**: Integration with cloud key management services
