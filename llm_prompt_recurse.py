import os
import sys
from dotenv import load_dotenv

ANTHROPIC_API_KEY = None

# Load the API key from the .env file
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def load_env():
    load_dotenv()
    global ANTHROPIC_API_KEY
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "":
        raise ValueError("API key is not set")

    print(f"Anthropic API key set.")

def main():
    load_env()
    print("Hello, world!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
