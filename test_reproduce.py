
import subprocess
import sys
import os

# Create a dummy script
with open("dummy.py", "w") as f:
    f.write("print('Hello')")

print(f"Running dummy.py with {sys.executable}")
# Run it with subprocess
try:
    subprocess.run([sys.executable, "dummy.py"], check=True)
except Exception as e:
    print(f"Error: {e}")
