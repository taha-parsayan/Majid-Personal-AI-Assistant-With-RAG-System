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
from rump import MajidRump

# Add the parent directory to the system path
current_path = os.getcwd()

#--------------------------------------------------
# Load environment variables
#--------------------------------------------------

'''
The goal is to make this project a .exe app.
Every time a separate file is used, we have to use the 
following code to set the current folder as base_path.
EVERY TIME!
'''
if getattr(sys, "_MEIPASS", False):
    base_path = sys._MEIPASS
else:
    base_path = os.getcwd()

env_path = os.path.join(base_path, ".env")

os.environ.pop("OPENAI_API_KEY", None) # Because it loads a key from some place I dont know!
os.environ.pop("TAVILY_API_KEY", None) # Because it loads a key from some place I dont know!
load_dotenv(env_path) 

#--------------------------------------------------
# Main
#--------------------------------------------------
if __name__ == "__main__":
    MajidRump().run()
