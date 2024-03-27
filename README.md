# llm-prompt-recurse

_NOTE_: This is my personal repo for testing prompt recursion in LLM. You can use this as a reference to implement prompt recursion in your own LLM fork.

This is based off of [langsmith-cookbook/assisted-prompt-engineering](https://github.com/langchain-ai/langsmith-cookbook/blob/main/optimization/assisted-prompt-bootstrapping/assisted-prompt-engineering.ipynb).

## Tests

https://twitter.com/mattshumer_/status/1773017544888082933

```plaintext
Matt Shumer
@mattshumer_
https://twitter.com/mattshumer_/status/1773017549803798999

THEAD

---

Introducing `claude-llm-trainer` ✍️

The world's simplest way to train a task-specific LLM.

Just write a sentence describing the model you want.

A chain of AI systems will generate a dataset and train a model for you.

And it's open-source.

https://twitter.com/i/status/1773017544888082933

---

How it works:

- The user describes the model they want
Ex: "A model that writes Python functions"

- claude-llm-trainer leverages a chain of Claude 3 calls to create a great dataset for your task.

- We process the dataset, and train a LLaMA model!

---

This was based off of an older project I did, so the model we train is LLaMA 2 7B.

If you want, you can easily use a newer + better model like Mistral 7B.

---

You can go from an idea to a fully trained model in a matter of minutes.

And the resulting models are really capable!

---

If you'd like to try it or contribute, check out the Github repo: https://t.co/LBAGQU2e0P
```
