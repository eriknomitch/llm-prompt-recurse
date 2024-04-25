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

DEFAULT_PROMPT_NAME = "eriknomitch/metaprompt"
DEFAULT_PROMPT_VERSION = "f8de889c"

ANTHROPIC_MODEL = "claude-3-opus-20240229"

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
def list_prompt_files():
    prompt_dir = 'prompts'
    files = [f for f in os.listdir(prompt_dir) if os.path.isfile(os.path.join(prompt_dir, f)) and f.endswith('.json')]
    return files

def load_json_from_prompts(filename):
    with open(os.path.join('prompts', filename), 'r') as file:
        return json.load(file)

def get_instructions(gen: str):
    return gen.split("<Instructions>")[1].split("</Instructions>")[0]

def print_overview(task, input_variables, output_variables, prompt_name, prompt_name_version):
    console = Console()
    console.print("[bold]Overview of Prompt Generation:[/bold]", style="green")
    console.print(f"• [bold]Prompt name/version:[/bold] {escape(prompt_name_version)}", style="yellow")
    console.print(f"• [bold]Task:[/bold] {escape(task)}", style="yellow")
    console.print(f"• [bold]Input variables:[/bold] {', '.join(map(escape, input_variables))}", style="yellow")
    console.print(f"• [bold]Prompt name:[/bold] {escape(prompt_name)}", style="yellow")
    console.print()  # For an extra newline for better separation

# --------------------------------------------------
# --------------------------------------------------
# --------------------------------------------------
def generate_meta_prompt(task: str, input_variables: list, output_variables: list, prompt_name: str, prompt_name_version: str, client=Client()):
    print("🟢 Generating meta prompt...")

    # The print_overview call is removed from here because it's already called in main_cli

    llm = ChatAnthropic(model=ANTHROPIC_MODEL)
    prompt = hub.pull(prompt_name_version)

    # Wrap each string in brackets and join by newline
    wrapped_input_variables = "\n".join([f"[{s}]" for s in input_variables])
    wrapped_output_variables = "\n".join([f"[{s}]" for s in output_variables])

    print("🟢 Running the pipeline...")

    with yaspin(text="Generating prompt..."):
        meta_prompter = prompt | llm | StrOutputParser() | get_instructions

        recommended_prompt = meta_prompter.invoke(
            {
                "task": (task),
                "input_variables": wrapped_input_variables,
                "output_variables": wrapped_output_variables,
            }
        )

    return recommended_prompt.strip()


@click.command()
@click.argument('prompt_filename', required=False)
def main(prompt_filename):

    if not prompt_filename:
        prompt_files = list_prompt_files()
        if not prompt_files:
            click.echo("No prompt files found in the 'prompts' directory.")
            sys.exit(1)
        prompt_filename = click.prompt("Please choose a prompt file", type=click.Choice(prompt_files, case_sensitive=False))

    try:
        if not prompt_filename.endswith('.json'):
            prompt_filename += '.json'

        prompt_filename_base = prompt_filename.removesuffix('.json')

        prompt_data = load_json_from_prompts(prompt_filename)
        task = prompt_data.get('task')
        input_variables = prompt_data.get('input_variables')
        output_variables = prompt_data.get('output_variables')
        prompt_name = prompt_data.get('prompt', {}).get('name', DEFAULT_PROMPT_NAME)
        prompt_version = prompt_data.get('prompt', {}).get('version', DEFAULT_PROMPT_VERSION)
        prompt_name_version = f"{prompt_name}:{prompt_version}" if prompt_version else prompt_name

        print_overview(task, input_variables, output_variables, prompt_name, prompt_name_version)

        if click.confirm('Do you want to generate the meta prompt?'):
            recommended_prompt = generate_meta_prompt(task, input_variables, output_variables, prompt_name, prompt_name_version)
            print(f"Recommended prompt:\n\n{recommended_prompt}")
            print()

            # Save the recommended prompt to './prompts/<prompt_name>.recommended.txt'
            with open(os.path.join('prompts', f"{prompt_filename_base}.recommended.txt"), 'w') as file:
                file.write(recommended_prompt)

            print(f"Recommended prompt saved to './prompts/{prompt_filename_base}.recommended.txt'")
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
    # Except a click exception to handle user cancellation
    except click.exceptions.Abort:
        print("Meta prompt generation cancelled by user.")
        sys.exit(0)
