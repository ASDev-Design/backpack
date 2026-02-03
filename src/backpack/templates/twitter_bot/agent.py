"""
Twitter Bot agent - uses Backpack-injected credentials and personality.
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
    logger = logging.getLogger("twitter_bot")

    openai_key = os.environ.get("OPENAI_API_KEY")
    twitter_token = os.environ.get("TWITTER_BEARER_TOKEN")
    system_prompt = os.environ.get("AGENT_SYSTEM_PROMPT", "")
    tone = os.environ.get("AGENT_TONE", "friendly")

    missing = [k for k in ("OPENAI_API_KEY", "TWITTER_BEARER_TOKEN") if not os.environ.get(k)]
    if missing:
        logger.error(f"Missing credentials: {', '.join(missing)}")
        logger.error("Add them with: backpack key add <KEY_NAME>")
        return

    logger.info("Twitter Bot agent ready")
    logger.info(f"Personality: {system_prompt[:60]}...")
    logger.info("\nIn a full implementation, you would:")
    logger.info("  - Use OPENAI_API_KEY for generating tweet text or replies")
    logger.info("  - Use TWITTER_BEARER_TOKEN with Twitter API v2 to post/read tweets")
    logger.info("  - Respect rate limits and Twitter rules. Customize this script for your bot.")


if __name__ == "__main__":
    main()