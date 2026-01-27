"""
Example agent implementation demonstrating Backpack integration.

This agent accesses injected credentials and personality variables
from the environment, which are provided by the Backpack system
during JIT variable injection.
"""

import os

def main():
    """
    Main agent function that uses injected environment variables.
    
    This demonstrates how an agent can access:
    - Credentials (API keys) from the keychain
    - Personality configuration (system prompts, tone)
    """
    # Access injected credentials
    openai_key = os.environ.get('OPENAI_API_KEY')
    twitter_token = os.environ.get('TWITTER_TOKEN')
    
    # Access injected personality
    system_prompt = os.environ.get('AGENT_SYSTEM_PROMPT')
    tone = os.environ.get('AGENT_TONE')
    
    print(f"Agent initialized with personality: {system_prompt}")
    print(f"Tone: {tone}")
    print(f"OpenAI Key available: {'Yes' if openai_key else 'No'}")
    print(f"Twitter Token available: {'Yes' if twitter_token else 'No'}")
    
    # Simulate agent work
    print("Agent is running...")

if __name__ == '__main__':
    main()