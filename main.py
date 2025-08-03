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
parent_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(parent_path)

#--------------------------------------------------
# Load environment variables
#--------------------------------------------------

os.environ.pop("OPENAI_API_KEY", None) # Because it loads a key from some place I dont know!
os.environ.pop("TAVILY_API_KEY", None) # Because it loads a key from some place I dont know!
load_dotenv(os.path.join(current_path, ".env")) 


#--------------------------------------------------
# Main
#--------------------------------------------------
if __name__ == "__main__":
    MajidRump().run()
