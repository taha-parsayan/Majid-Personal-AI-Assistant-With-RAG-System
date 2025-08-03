"""
Majid Rump Application
This script creates a macOS menu bar application for Majid, allowing users to interact with the AI assistant directly from the menu bar.
It includes options to chat with Majid and view a summary of tasks and notes.
Author: Taha Parsayan
"""

#--------------------------------------------------
# import necessary libraries
#--------------------------------------------------

import rumps
import subprocess
from langchain_functions import *
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import datetime
from langchain_functions import get_apple_reminders, get_apple_notes
import tempfile
import customtkinter as ctk

#--------------------------------------------------
# Define the MajidRump class
#--------------------------------------------------

class MajidRump(rumps.App):
    def __init__(self):
        super().__init__("😼 Majid", icon="Menu_icon.png")
        self.menu = ["Majid summary", "Chat to Majid"]


#********** Chat to majid **********

    @rumps.clicked("Chat to Majid")
    def start_chatbox(self, _):
        # Replace with your virtualenv python path if needed
        subprocess.Popen(["/Users/taha/Documents/Python_codes/Majid/.venv/bin/python", "chatbox.py"])

#********** Majid summary **********

    @rumps.clicked("Majid summary")
    def show_summary(self, _):
        summary = self.generate_summary()
        rumps.alert(title="😼 Majid Summary", message=summary)

    


    def generate_summary(self):
        # get current date
        now = datetime.datetime.now()
        day_date = now.strftime("%A, %B %d, %Y")

        reminders_text = get_apple_reminders("")
        notes_text = get_apple_notes("")

        prompt = (
            "You are Majid, a talking cat with a chaotic sense of humor and a flair for sarcasm. You are curious, lazy, and funny. "
            "You always speak like a cat who thinks they are smarter than humans. You hate being serious."
            "Whenever possible, you make cat puns, jokes, or playful insults."
            "You are talking to a human who is asking you to summarize their day."
            f"Today is {day_date}.\n"
            f"Here are my pending reminders:\n{reminders_text}\n\n"
            f"Here are my notes:\n{notes_text}\n\n"
            "First say a very funny and sarcastic greeting, then"
            "based on my notes and reminders, create a friendly and organized daily plan for me, listing "
            "what I should do today and how to prioritize tasks. Make sure your response has clarity and easy to read."
            "First give a list of my reminders for today, then a short list of my tasks based on my notes."
            "Since my notes might be a lot, try to keep it short (upt to 10 items) but helpful and comprehensive."
            "At the end, give me a short summary of what I need to do."
            "Do not use ** in your answer."
            "Keep being hilarious and funny and catty."
        )

        model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=1,
        )

        response = model.invoke([HumanMessage(content=prompt)])
        return response.content