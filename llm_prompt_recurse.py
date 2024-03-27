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
    
# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# TASK/VARIABLES -----------------------------------
# --------------------------------------------------
task = """Generate a LinkedIn post based on a Tweet (or series of tweets). It should include a 1.) a short, clear overview explaining the tweet(s) and 2.) a concrete example of how this could be leveraged by companies. It should be well crafted but avoid gimicks or over-reliance on buzzwords. Importantly, the post should be professional and informative in a matter-of-fact style. Avoid hype."""

input_variables = ["tweet"]

# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------
def get_instructions(gen: str):
    return gen.split("<Instructions>")[1].split("</Instructions>")[0]

def generate_meta_prompt(task: str, input_variables: list, client=Client(), prompt_name="wfh/metaprompt"):
    print("🟢 Generating meta prompt...")

    prompt = hub.pull(prompt_name)
    llm = ChatAnthropic(model="claude-3-opus-20240229")
   
    print(f" Task:\n{task}")
    print(f"Input variables:\n{input_variables}")
    print(f"Prompt name:\n{prompt_name}")

    # Wrap each string in brackets and join by newline
    wrapped_input_variables = "\n".join([f"[{s}]" for s in input_variables])
        
    print("🟢 Running the pipeline...")

    with yaspin(text="Generating prompt..."):
        meta_prompter = prompt | llm | StrOutputParser() | get_instructions

        recommended_prompt = meta_prompter.invoke(
            {
                "task": (task),
                "input_variables": wrapped_input_variables,
            }
        )

    return recommended_prompt

def main():

    try:
        recommended_prompt = generate_meta_prompt(task, input_variables)
        print(f"Recommended prompt:\n\n{recommended_prompt}")
        print()
    except Exception as e:
        debug()
        print(f"Error: {e}")
        raise e

if __name__ == "__main__":
    try:
        print("🟢 Starting...")
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
