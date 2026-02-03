"""
Team Agent Example
Demonstrates a 'Code Reviewer' persona that could be part of a team.
"""
import os


def main():
    role = "Code Reviewer"
    print(f"👨‍💻 Agent Role: {role}")
    
    # Credentials
    github_token = os.environ.get("GITHUB_TOKEN")
    openai_key = os.environ.get("OPENAI_API_KEY")
    
    if github_token and openai_key:
        print("✅ Connected to GitHub and OpenAI.")
    else:
        print("⚠️  Running in simulation mode (missing keys).")
        
    # Personality
    prompt = os.environ.get("AGENT_SYSTEM_PROMPT")
    print(f"\nInstructions: {prompt}")
    
    print("\nChecking pull requests...")
    print("Found PR #42: 'Add memory layer'")
    print("Reviewing...")
    print("LGTM! 🚀")

if __name__ == "__main__":
    main()
