"""
Backpack Visual Demo Script
Run this script to see a simulated demo of Backpack in action.
"""
import os
import sys
import time


def type_print(text, delay=0.03):
    """Simulate typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def step(text, pause=1.5):
    """Print a step description and pause."""
    print(f"\n👉 \033[1;36m{text}\033[0m")
    time.sleep(pause)

def run_command(cmd, output_lines):
    """Simulate running a shell command."""
    type_print(f"$ {cmd}", delay=0.05)
    time.sleep(0.5)
    for line in output_lines:
        print(line)
        time.sleep(0.1)
    time.sleep(1)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n🎒 \033[1;33mBackpack Agent Container Demo\033[0m\n")
    time.sleep(1)

    step("Scenario: You found an awesome agent on GitHub.")
    step("Problem: It needs API keys and configuration to run.")
    
    run_command("ls -l", [
        "total 8",
        "-rw-r--r--  1 user  staff  1234 Feb  2 10:00 agent.py",
        "-rw-r--r--  1 user  staff   850 Feb  2 10:00 agent.lock  <-- The Magic File 🔒",
        "-rw-r--r--  1 user  staff   450 Feb  2 10:00 requirements.txt"
    ])
    
    step("Let's try to run it with Backpack...")
    
    run_command("backpack run agent.py", [
        "Loading agent.lock...",
        "Found required credentials: OPENAI_API_KEY",
    ])
    
    step("Backpack detects the need for keys and checks your local vault.")
    
    print("\033[1;33m[Backpack] This agent requires 'OPENAI_API_KEY'.\033[0m")
    print("\033[1;33m           You have this key in your personal vault.\033[0m")
    type_print("           Allow access for this session? (Y/n) ", delay=0.05)
    time.sleep(1)
    type_print("Y", delay=0.2)
    
    print("\033[1;32m[OK] Key injected into process memory.\033[0m")
    time.sleep(0.5)
    
    print("\n🚀 \033[1;32mAgent is running...\033[0m")
    print("   Personality: Senior Financial Analyst")
    print("   Output: The stock market is showing bullish trends...")
    time.sleep(2)
    
    step("That's it! No .env files, no copy-pasting keys.")
    step("The agent traveled with its configuration, but your keys stayed safe.")
    
    print("\n✨ Try it yourself:")
    print("   pip install backpack")
    print("   backpack quickstart")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo cancelled.")
