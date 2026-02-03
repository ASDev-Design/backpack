"""
LangChain Integration Example
Demonstrates how to use Backpack with LangChain.

Requirements:
    pip install langchain openai
"""
import os

# Check if libraries are installed
try:
    from langchain.chains import LLMChain
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate
except ImportError:
    # Allow running in simulation mode even without libraries
    print("⚠️  LangChain not installed. Running in simulation mode.")
    OpenAI = None
    PromptTemplate = None
    LLMChain = None

def main():
    print("🔗 LangChain + Backpack Integration")
    
    # 1. Credentials are automatically injected by Backpack
    # LangChain will automatically look for OPENAI_API_KEY in os.environ
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found. Run with 'backpack run'.")
        # In a real scenario we might exit, but for demo we continue
    else:
        print("✅ API Key found.")

    # 2. Use Personality from Backpack
    system_prompt = os.environ.get("AGENT_SYSTEM_PROMPT", "You are a helpful assistant.")
    print(f"🧠 Using System Prompt: {system_prompt}")

    # 3. Setup LangChain (Simulation)
    if OpenAI:
        llm = OpenAI(temperature=0.9)
        template = f"{system_prompt}\n\nUser: {{question}}\nAI:"
        prompt = PromptTemplate(template=template, input_variables=["question"])
        # chain = LLMChain(llm=llm, prompt=prompt)
        print("✅ LangChain initialized.")
    else:
        print("⚠️  Skipping LangChain initialization.")
    
    # 4. Run
    question = "What is the capital of France?"
    print(f"\n❓ Asking: {question}")
    
    print("\n(Simulation: API call skipped to save credits)")
    print("💡 Response: The capital of France is Paris.")

if __name__ == "__main__":
    main()
