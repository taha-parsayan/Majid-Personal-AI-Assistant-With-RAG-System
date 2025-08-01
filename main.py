"""
This is the Majid
Majid: Management AI for Journals, Inbox, and Duties

Majid is an AI assistant designed to help us manage our journals, inbox, and duties efficiently. 
It uses advanced natural language processing techniques to understand our tasks and provide relevant responses.

Author: Taha Parsayan
"""

import os
import sys
from dotenv import load_dotenv
from langchain_functions import *

# Add the parent directory to the system path
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(parent_path)

# Load environment variables
os.environ.pop("OPENAI_API_KEY", None) # Because it loads a key from some place I dont know!
os.environ.pop("TAVILY_API_KEY", None) # Because it loads a key from some place I dont know!
load_dotenv(os.path.join(current_path, ".env")) 



# Main
if __name__ == "__main__":
    print("\n_______________Start Chattig with Majid_______________\n")

    chain = create_chain() # Create chain

    chat_history = load_chat_history_from_database() # Load chat history from database

    while True:
        user_input = input("You:\n")
        if user_input.lower() == "bye":
            print("\nMajid:\n", "See you later aligator!\n")
            break
        response = process_chat(chain, user_input, chat_history) # Process user input and get response
        chat_history.append(HumanMessage(content=user_input)) # Append user input to chat history
        chat_history.append(AIMessage(content=response)) # Append AI response to chat history
        save_message_in_database("human", user_input) # Save user input in database
        save_message_in_database("ai", response) # Save AI response in database
        print("\nMajid:\n", response)
        print("\n")