"""
Financial Analyst agent - uses Backpack-injected credentials and personality.
Run with: backpack run agent.py
"""

import json
import logging
import os


def main():
    # Setup basic logging
    deployment_config = json.loads(os.environ.get("AGENT_DEPLOYMENT_CONFIG", "{}"))
    logging_config = deployment_config.get("logging", {})
    level = getattr(logging, logging_config.get("level", "INFO").upper(), logging.INFO)
    logging.basicConfig(level=level, format=logging_config.get("format", "%(message)s"))
    logger = logging.getLogger("financial_analyst")

    api_key = os.environ.get("OPENAI_API_KEY")
    system_prompt = os.environ.get("AGENT_SYSTEM_PROMPT", "")
    tone = os.environ.get("AGENT_TONE", "formal")

    if not api_key:
        logger.error("OPENAI_API_KEY not found. Add it with: backpack key add OPENAI_API_KEY")
        return

    logger.info(f"Financial Analyst agent ready (tone: {tone})")
    logger.info(f"System prompt: {system_prompt[:80]}...")
    logger.info("\nIn a full implementation, you would:")
    logger.info("  - Call OpenAI/Anthropic with AGENT_SYSTEM_PROMPT as system message")
    logger.info("  - Process financial data (CSV, APIs) and ask the model for analysis")
    logger.info("  - Return structured reports. Customize this script for your use case.")


if __name__ == "__main__":
    main()