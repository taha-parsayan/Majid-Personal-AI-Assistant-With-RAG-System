"""
This is the Majid
Majid: Management AI for Journals, Inbox, and Duties

Majid is an AI assistant designed to help us manage our journals, inbox, and duties efficiently. 
It uses advanced natural language processing techniques to understand our tasks and provide relevant responses.

Author: Taha Parsayan
"""

#--------------------------------------------------
# Import libraries
#--------------------------------------------------

import os
import sys
from dotenv import load_dotenv
from langchain_functions import *
import threading
import customtkinter as ctk
from GUI import run_gui

# Add the parent directory to the system path
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(parent_path)

#--------------------------------------------------
# Load environment variables
#--------------------------------------------------

os.environ.pop("OPENAI_API_KEY", None) # Because it loads a key from some place I dont know!
os.environ.pop("TAVILY_API_KEY", None) # Because it loads a key from some place I dont know!
load_dotenv(os.path.join(current_path, ".env")) 

#--------------------------------------------------
# Chat functions
#--------------------------------------------------

def text_chat_loop(chain, chat_history):
    while True:
        user_input = input("You:\n")
        if user_input.lower() == "bye":
            print("\nMajid:\n", "See you later alligator!\n")
            break
        response = process_chat(chain, user_input, chat_history)
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))
        save_message_in_database("human", user_input)
        save_message_in_database("ai", response)
        print("\nMajid:\n", response)
        print("\n")

#--------------------------------------------------
# Main
#--------------------------------------------------
if __name__ == "__main__":
    print("\n_______________Start Chattig with Majid_______________\n")

    chain = create_chain()
    chat_history = load_chat_history_from_database()

    run_gui(chain, chat_history)  # GUI runs on main thread