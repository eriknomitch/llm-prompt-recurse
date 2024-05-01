import json
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

# Initialize the Anthropic chat model
chat_model = ChatAnthropic(api_key="your_api_key_here", model="claude-3-sonnet-20240229", temperature=0.2)

# Load JSON data from a file named 'data.json'
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to process and display the loaded data using the chat model
def process_data(data, chat_model):
    system_message = data['system']
    messages = data['messages']

    # Define the chat prompt template dynamically based on the loaded messages
    prompts = [("system", system_message)]
    for message in messages:
        if message['type'] == 'human':
            prompts.append(("human", message['text']))

    chat_template = ChatPromptTemplate.from_messages(prompts)

    # Start the chat by invoking the model
    response = chat_model.invoke(chat_template.to_prompt())
    print("Response from model:", response)

# Main execution
if __name__ == "__main__":
    file_path = 'chats/cover_letter.json'
    data = load_json_data(file_path)
    process_data(data, chat_model)

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
