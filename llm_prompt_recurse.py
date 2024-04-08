import os
import sys
import time

import click
from rich.console import Console
from rich.markup import escape
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
task = """Generate a LinkedIn post based on formatted text from Tweet(s). It should be well crafted but avoid gimicks or over-reliance on buzzwords."""

input_variables = ["tweet"]

prompt_name = "eriknomitch/metaprompt"
prompt_version = "e6cc56a0"
prompt_name_version = prompt_name + f":{prompt_version}" if prompt_version else ''

# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------
def get_instructions(gen: str):
    return gen.split("<Instructions>")[1].split("</Instructions>")[0]

def print_overview(task, input_variables, prompt_name_version):
    console = Console()
    console.print("[bold]Overview of Prompt Generation:[/bold]", style="green")
    console.print(f"• [bold]Prompt name/version:[/bold] {escape(prompt_name_version)}", style="yellow")
    console.print(f"• [bold]Task:[/bold] {escape(task)}", style="yellow")
    console.print(f"• [bold]Input variables:[/bold] {', '.join(map(escape, input_variables))}", style="yellow")
    console.print(f"• [bold]Prompt name:[/bold] {escape(prompt_name)}", style="yellow")
    console.print()  # For an extra newline for better separation

def generate_meta_prompt(task: str, input_variables: list, client=Client()):
    print("🟢 Generating meta prompt...")

    print_overview(task, input_variables, prompt_name_version)

    
    llm = ChatAnthropic(model="claude-3-opus-20240229")
    prompt = hub.pull(prompt_name_version)
   
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
        print_overview(task, input_variables, prompt_name_version)
        if click.confirm('Do you want to generate the meta prompt?'):
            recommended_prompt = generate_meta_prompt(task, input_variables)
            print(f"Recommended prompt:\n\n{recommended_prompt}")
            print()
        else:
            print("Meta prompt generation cancelled by user.")
            sys.exit(0)
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
