"""
Stateful Agent Example
An agent that remembers information between runs using Backpack's encrypted memory.
"""
from backpack.agent_lock import AgentLock


def main():
    print("🧠 Stateful Agent Starting...")
    
    # Initialize AgentLock to access memory
    # Note: In a future version, memory might be injected/exposed more easily.
    # For now, we use the SDK to read/write memory.
    lock = AgentLock("agent.lock")
    agent_data = lock.read()
    
    if not agent_data:
        print("❌ No agent.lock found. Run via 'backpack run' or ensure agent.lock exists.")
        return

    memory = agent_data.get("memory", {})
    
    # Read existing state
    run_count = memory.get("run_count", 0)
    last_message = memory.get("last_message", "None")
    
    print("\n📊 Memory State:")
    print(f"   - Run Count: {run_count}")
    print(f"   - Last Message: {last_message}")
    
    # Update state
    new_count = run_count + 1
    new_message = f"Hello from run #{new_count}"
    
    print(f"\nUpdating memory -> Run Count: {new_count}")
    
    memory["run_count"] = new_count
    memory["last_message"] = new_message
    
    # Save encrypted memory
    try:
        lock.update_memory(memory)
        print("✅ Memory saved successfully (Encrypted).")
    except Exception as e:
        print(f"❌ Failed to save memory: {e}")

if __name__ == "__main__":
    main()
