# Agent Deployment Template

This template is designed for production-ready agent deployments. It comes pre-configured with support for:

- **Network Settings**: Host, port, proxy configurations.
- **Resource Management**: CPU and memory limits.
- **Security Policies**: Domain allowlists and access controls.
- **Logging**: Structured logging configuration.

## Usage

1. Initialize:
   ```bash
   backpack template use agent_deployment
   ```

2. Add Credentials:
   ```bash
   backpack key add OPENAI_API_KEY
   ```

3. Run:
   ```bash
   backpack run agent.py
   ```

## Configuration

The configuration is stored in `agent.lock` under the `deployment` layer. It is injected into the agent environment as `AGENT_DEPLOYMENT_CONFIG`.
