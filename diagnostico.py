import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Path: {sys.path}")

try:
    import chromadb
    print(f"SUCCESS: chromadb version {chromadb.__version__} is available.")
except ImportError:
    print("FAILURE: chromadb is NOT available in this environment.")

print("\n--- Pip List (limited) ---")
os.system(f'"{sys.executable}" -m pip list | grep -E "chromadb|gradio|openai"')
