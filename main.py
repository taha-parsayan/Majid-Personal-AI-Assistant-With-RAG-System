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
import subprocess
from dotenv import load_dotenv
from rump import MajidRump

#--------------------------------------------------
# Load environment variables
#--------------------------------------------------

'''
The goal is to make this project a .exe app.
Every time a separate file is used, we have to use the 
following code to set the current folder as base_path.
EVERY TIME!
'''

'''
# For app deployment:

if getattr(sys, "_MEIPASS", False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(base_path, ".env")
load_dotenv(dotenv_path=env_path)
'''

# For .exe:
# Use a persistent, writable directory
user_dir = os.path.expanduser("~/Library/Application Support/Majid")
os.makedirs(user_dir, exist_ok=True)

env_path = os.path.join(user_dir, ".env")

# Load .env (create if missing)
if not os.path.exists(env_path):
    with open(env_path, "w") as f:
        f.write("OPENAI_API_KEY=\n")
        f.write("TAVILY_API_KEY=\n")

os.environ.pop("OPENAI_API_KEY", None) # Because it loads a key from some place I dont know!
os.environ.pop("TAVILY_API_KEY", None) # Because it loads a key from some place I dont know!
load_dotenv(env_path) 

#--------------------------------------------------
# Main
#--------------------------------------------------
if __name__ == "__main__":
    MajidRump().run()
