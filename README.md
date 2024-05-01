# llm-prompt-recurse

_NOTE_: This is my personal repo for testing prompt recursion in LLM. You can use this as a reference to implement prompt recursion in your own LLM fork.

## Summary

This repository is dedicated to exploring and testing prompt recursion with large language models (LLMs). It includes a collection of JSON and text files that define various tasks for LLMs, such as generating emails, analyzing job fit, and creating resumes. The repository also contains a Python script (`interactive.py`) for interacting with the prompts, and a Python package configuration file (`pyproject.toml`).

The main focus is to refine the process of prompt engineering by using meta-prompts, which are prompts that instruct an LLM to generate other prompts. This recursive approach aims to streamline the creation of effective prompts for various tasks.

The `prompts` directory contains the JSON files that define the tasks, while the `examples.toml` file provides a list of example tasks in TOML format. The `llm_prompt_recurse.py` script is used to generate meta-prompts based on the JSON task definitions.

This project is a personal endeavor and serves as a practical reference for anyone interested in implementing prompt recursion in their own projects with LLMs.

(This is based off of [langsmith-cookbook/assisted-prompt-engineering](https://github.com/langchain-ai/langsmith-cookbook/blob/main/optimization/assisted-prompt-bootstrapping/assisted-prompt-engineering.ipynb) but has now diverted significantly.)
