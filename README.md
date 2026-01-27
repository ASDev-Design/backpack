# Backpack: Encrypted Agent Container System

**Backpack** is a secure, portable system for managing AI agents with encrypted state, credentials, and personality configurations. It solves the "Naked Agent" problem by providing a unified container format that travels with your agent code in version control.

## Table of Contents

- [The Problem](#the-problem-the-naked-agent)
- [The Solution](#the-solution-encrypted-agent-containers)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Security](#security)
- [Contributing](#contributing)

## The Problem: "The Naked Agent"

Right now, an agent is just code. It has no state and no keys until a developer manually injects them.

- **Code**: Public (GitHub)
- **Secrets**: Private (Scattered in `.env` or cloud dashboards)
- **Memory**: Private (Stuck in a specific vector database)

This creates friction when sharing agents, managing credentials, and maintaining state across environments.

## The Solution: Encrypted Agent Containers

Backpack creates an `agent.lock` file that travels with the agent's code in the git repo. This file contains three distinct encrypted "variable" layers:

### Layer 1: Credentials (The Keys)

**Content**: Placeholders for `OPENAI_API_KEY`, `TWITTER_TOKEN`, etc.

**Innovation**: When a user clones the agent, the system sees the `agent.lock`. It checks the user's personal local keychain. If the user has a "Global OpenAI Key" saved, it automatically injects it into the agent's encrypted runtime. No manual `.env` setup required.

### Layer 2: Personality & System Prompts (The Brain)

**Content**: "You are a senior financial analyst. Use a formal tone."

**Innovation**: These are variables that can be tweaked and version-controlled. A team can update the "Personality Variable" in Git, and everyone's local agent updates instantly upon `git pull`.

### Layer 3: Ephemeral Memory (The Context)

**Content**: User ID, Session History, last tool output.

**Innovation**: Local-first memory. The agent writes its "short-term memory" to an encrypted local file. This means you can stop an agent on your laptop, commit the encrypted state, push it to a server, and the agent resumes exactly where it left off.

## Features

- 🔐 **Encrypted State Management**: All agent data is encrypted using PBKDF2 and Fernet
- 🔑 **OS Keychain Integration**: Secure credential storage using platform-native keyrings
- 🚀 **JIT Variable Injection**: Just-in-time credential injection with user consent
- 📦 **Portable Containers**: `agent.lock` files travel with your code in version control
- 🧠 **Version-Controlled Personality**: System prompts and configuration in Git
- 💾 **Ephemeral Memory**: Encrypted state that can be committed and shared
- 🛡️ **No Plain Text Secrets**: Keys never written to disk in plain text

## Installation

### Prerequisites

- Python 3.7+
- pip

### Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd backpack

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
python backpack.py --help
```

## Quick Start

1. **Add keys to your personal vault:**
   ```bash
   python backpack.py key add OPENAI_API_KEY
   python backpack.py key add TWITTER_TOKEN
   ```

2. **Initialize an agent:**
   ```bash
   python backpack.py init --credentials "OPENAI_API_KEY,TWITTER_TOKEN" --personality "You are a senior financial analyst. Use a formal tone."
   ```

3. **Run the agent:**
   ```bash
   python backpack.py run example_agent.py
   ```

For detailed usage instructions, see [USAGE.md](USAGE.md).

## Project Structure

```
backpack/
├── backpack.py           # Main CLI entry point
├── example_agent.py      # Example agent implementation
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── USAGE.md             # Usage guide
├── ARCHITECTURE.md      # Architecture documentation
├── SECURITY.md          # Security considerations
├── CONTRIBUTING.md      # Contributing guidelines
└── src/
    ├── __init__.py      # Package initialization
    ├── agent_lock.py    # Agent lock file management
    ├── cli.py           # CLI command definitions
    ├── crypto.py        # Encryption/decryption utilities
    └── keychain.py      # OS keychain integration
```

## Architecture

Backpack implements a three-layer encryption system:

1. **Credentials Layer**: Stores placeholders for required API keys
2. **Personality Layer**: Stores system prompts and agent configuration
3. **Memory Layer**: Stores ephemeral agent state

All layers are encrypted using PBKDF2 key derivation and Fernet symmetric encryption. The master key can be set via the `AGENT_MASTER_KEY` environment variable.

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).

## Documentation

- **[USAGE.md](USAGE.md)**: Detailed usage guide with examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System architecture and design decisions
- **[SECURITY.md](SECURITY.md)**: Security considerations and best practices
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Guidelines for contributing to the project
- **[PROJECT_ASSESSMENT.md](PROJECT_ASSESSMENT.md)**: Comprehensive project assessment and gap analysis

## Security

Backpack prioritizes security through:

- Encrypted storage of all agent data
- OS-native keychain integration
- No plain text secrets on disk
- User consent prompts for credential access

For detailed security information, see [SECURITY.md](SECURITY.md).

## The "JIT" Variable Injection Workflow

This is where the "GitHub of Secret Management" thinking revolutionizes agents.

### Current Workflow (Bad):

1. Agent tries to run
2. Agent crashes because `TWITTER_API_KEY` is missing
3. User goes to Twitter Developer Portal, generates key, pastes into `.env`
4. Restart

### Backpack "Agent Passport" Workflow:

1. Agent initializes
2. It reads `agent.lock` and sees it needs `TWITTER_API_KEY`
3. **Intervention**: Instead of crashing, the CLI pauses execution and prompts:
   ```
   This agent requires access to Twitter. You have a Twitter key in your personal vault. Allow access? (Y/n)
   ```
4. **Grant**: User hits 'Y'. The CLI decrypts the key only into the agent's process memory
5. The agent runs. The key is never written to disk in plain text

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Code style and standards
- Testing requirements
- Pull request process
- Development setup

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Assessment

For a detailed assessment of the project's current state, strengths, gaps, and recommendations, see [PROJECT_ASSESSMENT.md](PROJECT_ASSESSMENT.md).

## Support

For issues, questions, or contributions, please open an issue on the repository.
