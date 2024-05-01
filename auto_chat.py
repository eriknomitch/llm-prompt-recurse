import os
import toml
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from ipdb import set_trace

load_dotenv()

# Initialize the Anthropic chat model
chat_model = ChatAnthropic(api_key=os.getenv('ANTHROPIC_API_KEY'), model="claude-3-sonnet-20240229", temperature=0)

# Load JSON data from a file named 'data.json'
def load_toml_data(file_path):
    with open(file_path, 'r') as file:
        return toml.load(file)

def invoke_chain(prompts):
    prompt_template = ChatPromptTemplate.from_messages(prompts)

    chain = prompt_template | chat_model

    # Make a dict `inputs` from the file 'chats/cover_letter.inputs.toml'
    inputs_path = 'chats/cover_letter.inputs.toml'
    inputs = load_toml_data(inputs_path)

    # Print only the keys and of the inputs
    print("Inputs:", inputs.keys())
    
    chain = ChatPromptTemplate.from_messages(prompts) | chat_model

    message = chain.invoke(inputs)
    content = message.content

    return message


# Function to process and display the loaded data using the chat model
def process_data(system_message, messages, chat_model, prompts=[], index=0):

    print(f"Processing message {index + 1} of {len(messages)}")

    if index == 0:
        prompts.append(("system", system_message))

    # Append the first human message to the prompts
    prompts.append(("human", messages[index]['text']))

    response = invoke_chain(prompts)

    print("-------------------------------")
    print("Response:", response.content)
    print("-------------------------------")

    # If there are more messages to process, recursively call the function
    if index + 1 < len(messages):
        prompts.append(("ai", response.content))
        return process_data(system_message, messages, chat_model, prompts=prompts, index=(index + 1))

    print("Chat completed!")

    set_trace()

# Main execution
if __name__ == "__main__":
    file_path = 'chats/cover_letter.toml'
    data = load_toml_data(file_path)
    system_message = data['system']['description']
    messages = data['messages']
    process_data(system_message, messages, chat_model)
