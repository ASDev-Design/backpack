"""
Multi-Key Agent Example
An agent that requires multiple credentials (e.g., LLM + Social Media).
"""
import os
import sys


def main():
    print("🐦 Twitter Bot Agent Starting...")
    
    # Required keys
    required_keys = ["OPENAI_API_KEY", "TWITTER_TOKEN"]
    missing_keys = []
    
    for key in required_keys:
        value = os.environ.get(key)
        if value:
            print(f"✅ {key} loaded.")
        else:
            print(f"❌ {key} missing.")
            missing_keys.append(key)
            
    if missing_keys:
        print(f"\nMissing keys: {', '.join(missing_keys)}")
        print("Please add them using 'backpack key add <KEY_NAME>'")
        sys.exit(1)
        
    print("\n🚀 All systems go!")
    print("   - LLM: Connected")
    print("   - Twitter: Connected")
    
    # Access Personality
    prompt = os.environ.get("AGENT_SYSTEM_PROMPT", "")
    print(f"\n📝 Posting strategy: {prompt}")
    
    print("\n(Simulation: Generating tweet...)")
    print("Tweet posted: 'Hello world! #AI #Backpack'")

if __name__ == "__main__":
    main()
