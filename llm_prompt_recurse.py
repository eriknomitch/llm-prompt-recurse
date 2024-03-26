import os
import sys
import time

from dotenv import load_dotenv
from langsmith import Client

from langchain import hub
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser

from ipdb import set_trace as debug

from yaspin import yaspin

ANTHROPIC_API_KEY = None

# Load the API key from the .env file
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def load_env():
    load_dotenv()
    global ANTHROPIC_API_KEY
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "":
        raise ValueError("API key is not set")

    print(f"✅ Anthropic API key set.")

def get_instructions(gen: str):
    return gen.split("<Instructions>")[1].split("</Instructions>")[0]


def main():
    load_env()
    print("Hello, world!")

    try:

        client = Client()

        task = (
            """Generate a LinkedIn post to summarize AI news. It should be well crafted but avoid gimicks or over-reliance on buzzwords."""
        )

        print(f"Task: {task}")

        prompt = hub.pull("wfh/metaprompt")
        llm = ChatAnthropic(model="claude-3-opus-20240229")

        print("🚀 Running the pipeline...")

        with yaspin(text="Generating prompt..."):
            meta_prompter = prompt | llm | StrOutputParser() | get_instructions

        recommended_prompt = meta_prompter.invoke(
            {
                "task": task,
                "input_variables": """
    {paper}
    """,
            }
        )
        print(recommended_prompt)
    except Exception as e:
        debug()
        print(f"Error: {e}")
        raise e

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
