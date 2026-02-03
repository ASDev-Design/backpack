"""
Basic Agent Example
A simple agent that uses a single credential and a system prompt.
"""
import os
import sys


def main():
    print("🤖 Basic Agent Starting...")
    
    # 1. Access Credentials
    # Backpack injects these into the environment process-only
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found.")
        print("   Run 'backpack key add OPENAI_API_KEY' to add it to your vault.")
        sys.exit(1)
        
    print(f"✅ Credentials found: OPENAI_API_KEY present (Length: {len(api_key)})")
    
    # 2. Access Personality
    # Backpack injects this from the 'personality' layer in agent.lock
    system_prompt = os.environ.get("AGENT_SYSTEM_PROMPT", "Default prompt")
    tone = os.environ.get("AGENT_TONE", "Default tone")
    
    print("🧠 Personality loaded:")
    print(f"   - System Prompt: {system_prompt}")
    print(f"   - Tone: {tone}")
    
    # 3. Simulate Agent Logic
    print("\n💬 Agent is ready to chat!")
    print("(This is a simulation. In a real agent, you would call the OpenAI API here.)")

if __name__ == "__main__":
    main()
