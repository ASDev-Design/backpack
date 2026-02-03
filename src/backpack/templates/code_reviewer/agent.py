"""
Code Reviewer agent - uses Backpack-injected credentials and personality.
Run with: backpack run agent.py
"""

import os
import logging
import json

def main():
    # Setup basic logging (can be enhanced with injected config)
    deployment_config = json.loads(os.environ.get("AGENT_DEPLOYMENT_CONFIG", "{}"))
    logging_config = deployment_config.get("logging", {})
    level = getattr(logging, logging_config.get("level", "INFO").upper(), logging.INFO)
    logging.basicConfig(level=level, format=logging_config.get("format", "%(message)s"))
    logger = logging.getLogger("code_reviewer")

    api_key = os.environ.get("OPENAI_API_KEY")
    system_prompt = os.environ.get("AGENT_SYSTEM_PROMPT", "")
    tone = os.environ.get("AGENT_TONE", "professional")

    if not api_key:
        logger.error("OPENAI_API_KEY not found. Add it with: backpack key add OPENAI_API_KEY")
        return

    logger.info("Code Reviewer agent ready")
    logger.info(f"System prompt: {system_prompt[:70]}...")
    logger.info("\nIn a full implementation, you would:")
    logger.info("  - Read diff or file content (e.g. from stdin or path)")
    logger.info("  - Send to your LLM with AGENT_SYSTEM_PROMPT as system message")
    logger.info("  - Output review comments (inline or summary). Customize this script.")


if __name__ == "__main__":
    main()