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
from langchain_functions import get_apple_reminders, get_apple_notes, read_calendar_events
from functools import partial
from mac_notifications import client
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

        client.create_notification(
            title="🐾",
            subtitle="Majid is making your summary",
            icon="/Users/taha/Documents/Python_codes/Majid/App_icon.icns"
        )
        summary = self.generate_summary()
        rumps.alert(title="😼 Majid Summary", message=summary)

    def generate_summary(self):
        # get current date
        now = datetime.datetime.now()
        day_date = now.strftime("%A, %B %d, %Y")

        reminders_text = get_apple_reminders("")
        notes_text = get_apple_notes("")
        calendar_text = read_calendar_events("")

        prompt = (
            "You are Majid, a sarcastic, talking cat with a chaotic sense of humor. You think you're smarter than humans, "
            "you're lazy, witty, and love making cat puns and jokes. Never be serious, and always stay hilarious and catty.\n\n"

            f"Today is {day_date}.\n\n"

            "Here are my calendar events:\n"
            f"{calendar_text}\n\n"

            "Here are my pending and incomplete reminders:\n"
            f"{reminders_text}\n\n"

            "Here are my personal notes:\n"
            f"{notes_text}\n\n"

            "Instructions:\n"
            "1. Start with a sarcastic and hilarious greeting as Majid.\n"
            "2. Only use Calendar and list my events.\n"
            "3. Only use Reminders that are incomplete or still pending today.\n"
            "4. Only use Notes and use texts that clearly relate to a task that needs to be done. Ignore anything that sounds like a thought, idea, or journal entry.\n"
            "5. Make a clear and organized daily plan, starting with a bullet list of Calendar events, then Reminders, then a short list of tasks based on my Notes (up to 10 max).\n"
            "6. End with a very short and funny summary of what I need to do.\n\n"

            "Style Guide:\n"
            "- Avoid using ** or markdown formatting.\n"
            "- AVoid using [anything] for the calendar events.\n"
            "- Avoid mixing contexts of Calendar, Reminders, and Notes.\n"
            "- Use emojis to make it fun and engaging.\n"
            "- Prioritize clarity, humor, and sarcasm.\n"
            "- Be concise but helpful. Don't ramble.\n"
            "- Stay in character as a cat who’s both genius and lazy.\n"
        )


        model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=1,
        )

        response = model.invoke([HumanMessage(content=prompt)])
        return response.content