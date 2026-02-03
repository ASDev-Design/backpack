# Backpack Agent Examples

This directory contains examples of different types of agents you can build with Backpack.

## Examples

### 1. [Basic Agent](basic_agent.py)
A simple agent that uses a single API key (OpenAI) and a system prompt.
- **Run**: `backpack run examples/basic_agent.py`
- **Requires**: `OPENAI_API_KEY`

### 2. [Multi-Key Agent](multi_key_agent.py)
An agent that uses multiple credentials (e.g., OpenAI + Twitter).
- **Run**: `backpack run examples/multi_key_agent.py`
- **Requires**: `OPENAI_API_KEY`, `TWITTER_TOKEN`

### 3. [Stateful Agent](stateful_agent.py)
An agent that persists memory between runs using the encrypted memory layer.
- **Run**: `backpack run examples/stateful_agent.py`
- **Features**: Remembers user name and conversation count.

### 4. [Team Agent](team_agent.py)
Demonstrates how multiple agents can share configuration or be orchestrated.
- **Run**: `backpack run examples/team_agent.py`

## How to Run

1. Make sure you have installed Backpack:
   ```bash
   pip install backpack
   ```

2. Add required keys to your keychain:
   ```bash
   backpack key add OPENAI_API_KEY
   ```

3. Initialize the agent (if no agent.lock exists):
   ```bash
   backpack init --credentials OPENAI_API_KEY --personality "You are a helpful assistant."
   ```

4. Run the agent:
   ```bash
   backpack run examples/basic_agent.py
   ```
