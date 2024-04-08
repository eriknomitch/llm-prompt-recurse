import os
import sys
import time
import json

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
# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------
def load_json_from_prompts(filename):
    with open(os.path.join('prompts', filename), 'r') as file:
        return json.load(file)

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

def generate_meta_prompt(task: str, input_variables: list, prompt_name_version: str, client=Client()):
    print("🟢 Generating meta prompt...")

    # The print_overview call is removed from here because it's already called in main_cli


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


@click.command()
@click.argument('prompt_filename')
def main(prompt_filename):
    prompt_data = load_json_from_prompts(prompt_filename)
    task = prompt_data.get('task')
    input_variables = prompt_data.get('input_variables')
    prompt_name = prompt_data.get('prompt', {}).get('name')
    prompt_version = prompt_data.get('prompt', {}).get('version')
    prompt_name_version = f"{prompt_name}:{prompt_version}" if prompt_version else prompt_name

    try:
        print_overview(task, input_variables, prompt_name_version)
        if click.confirm('Do you want to generate the meta prompt?'):
            recommended_prompt = generate_meta_prompt(task, input_variables, prompt_name_version)
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
        else:
        print("Meta prompt generation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        debug()
        print(f"Error: {e}")
        raise e

