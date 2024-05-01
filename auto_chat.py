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
    print("Prompts:", prompts)

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
def process_data(system_message, messages, chat_model, prompts=[]):

    if len(prompts) == 0:
        prompts.append(("system", system_message))

    for message in messages:
        if message['type'] == 'human':
            prompts.append(("human", message['text']))
        elif message['type'] == 'ai' and message['text'] is False:
            break

    response = invoke_chain(prompts)

    print("-------------------------------")
    print("Response:", response.content)
    print("-------------------------------")

    # If there are more messages to process, recursively call the function
    if len(messages) < len(data['messages']):
        return process_data(data, chat_model, prompts.append(("ai", response.content)))

    print("Chat completed!")

    set_trace()

# Main execution
if __name__ == "__main__":
    file_path = 'chats/cover_letter.toml'
    data = load_toml_data(file_path)
    system_message = data['system']['description']
    messages = data['messages']
    process_data(system_message, messages, chat_model)
# import json
#
# from langchain_anthropic import ChatAnthropic
# from langchain.memory import ConversationBufferMemory
# from langchain_core.prompts import (
#     ChatPromptTemplate,
#     FewShotChatMessagePromptTemplate,
# )
#
#
# # Initialize the Anthropic chat model
# chat = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.2)
#
# # Set up conversation memory
# memory = ConversationBufferMemory(memory_key="chat_history")
#
# # Define the chat prompt template
# chat_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", "You are a helpful AI bot. Your name is {name}."),
#         ("human", "Hello, how are you doing?"),
#         ("ai", "I'm doing well, thanks!"),
#         ("human", "{user_input}"),
#     ]
# )
#
# messages = chat_template.format_messages(name="BoltAI", user_input="What is your name?")
#
# # Start the chat
# chat.start_conversation(
#     prompt=prompt,
#     chat_memory=memory,
#     chat_template=chat_template,
#     messages=messages,
# )
#
# # Load JSON data from a file named 'data.json'
# def load_json_data(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)
#
# # Example function to process and display the loaded data
# def process_data(data):
#     system_message = data['system']
#     print("System Description:", system_message)
#
#     for message in data['messages']:
#         if message['type'] == 'human':
#             print("Message from human:", message['text'])
#
# # Main execution
# if __name__ == "__main__":
#     file_path = 'data.json'  # Assuming 'data.json' is in the same directory as this script
#     data = load_json_data(file_path)
#     process_data(data)
#
