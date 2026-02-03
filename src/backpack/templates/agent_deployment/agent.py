"""
Agent Deployment Template - fully configured for production environments.
"""

import os
import json
import logging
import sys

# Configure logging based on injected config if available
def setup_logging(config):
    logging_config = config.get("logging", {})
    level_name = logging_config.get("level", "INFO").upper()
    format_str = logging_config.get("format", "%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level, format=format_str)
    return logging.getLogger("agent")

def main():
    # 1. Load Deployment Configuration
    deployment_config_str = os.environ.get("AGENT_DEPLOYMENT_CONFIG", "{}")
    try:
        deployment_config = json.loads(deployment_config_str)
    except json.JSONDecodeError:
        print("Error: AGENT_DEPLOYMENT_CONFIG is not valid JSON", file=sys.stderr)
        deployment_config = {}

    # 2. Setup Logging
    logger = setup_logging(deployment_config)
    logger.info("Agent starting up...")

    # 3. Access Configuration
    network_config = deployment_config.get("network", {})
    resources_config = deployment_config.get("resources", {})
    security_config = deployment_config.get("security", {})

    # In a real agent, you might bind to this host/port
    logger.info(f"Loaded configuration for host: {network_config.get('host', 'unknown')}")
    logger.info(f"Resource limits - CPU: {resources_config.get('cpu_limit', 'N/A')}, Memory: {resources_config.get('memory_limit', 'N/A')}")

    # 4. Access Credentials & Personality
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not found")
    else:
        logger.info("OPENAI_API_KEY is present")
    
    system_prompt = os.environ.get("AGENT_SYSTEM_PROMPT", "")
    tone = os.environ.get("AGENT_TONE", "professional")
    
    logger.info(f"Personality loaded. Tone: {tone}")
    logger.info(f"System Prompt: {system_prompt[:50]}...")

    # 5. Agent Logic
    logger.info("Agent is ready to accept tasks.")
    # ... your agent loop here ...

if __name__ == "__main__":
    main()