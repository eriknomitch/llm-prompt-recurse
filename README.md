# llm-prompt-recurse

_NOTE_: This is my personal repo for testing prompt recursion in LLM. You can use this as a reference to implement prompt recursion in your own LLM fork.

## Summary

The main focus is to refine the process of prompt engineering by using meta-prompts, which are prompts that instruct an LLM to generate other prompts. This recursive approach aims to streamline the creation of effective prompts for various tasks.

The `prompts` directory contains the JSON files that define the tasks, The `llm_prompt_recurse.py` script is used to generate meta-prompts based on the JSON task definitions.

---

_NOTE:_ This project is a personal endeavor and serves as a practical reference for anyone interested in implementing prompt recursion in their own projects with LLMs. Its based off of [langsmith-cookbook/assisted-prompt-engineering](https://github.com/langchain-ai/langsmith-cookbook/blob/main/optimization/assisted-prompt-bootstrapping/assisted-prompt-engineering.ipynb) but has now diverted significantly.

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd llm-prompt-recurse
```

2. Install the required packages:

```bash
poetry install
```

## Usage

1. Define the tasks in the `prompts` directory. Each task is defined in a separate JSON file at `tasks/<task-name>.json`. See `prompts/examples.json` for examples.

2. Run the script:

```bash
poetry run python llm_prompt_recurse.py <task-name>
```

This generates a meta-prompt for the specified task based on the JSON definition.
