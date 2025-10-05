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
import pync
import os
import sys
import random
from dotenv import load_dotenv
import subprocess


class MajidRump(rumps.App):
    def __init__(self):
        super().__init__("😼 Majid", icon="icons/Menu_icon.png")
        self.menu = ["Majid summary", "Chat to Majid", "Set API keys"]

        self.current_path = os.getcwd()

        #--------------------------------------------------
        # Define the MajidRump class
        #--------------------------------------------------

    #********** Chat to majid **********

    @rumps.clicked("Chat to Majid")
    def start_chatbox(self, _):
        try:
            subprocess.Popen([sys.executable, "chatbox_WEB.py"])
        except Exception as e:
            rumps.alert("Error", f"Failed to open API key entry: {str(e)}")

    #********** Set API keys **********

    @rumps.clicked("Set API keys")
    def set_api_keys(self, _):
        try:
            subprocess.Popen([sys.executable, "enter_api_WEB.py"])
        except Exception as e:
            rumps.alert("Error", f"Failed to open API key entry: {str(e)}")


    #********** Majid summary **********
    
    @rumps.clicked("Majid summary")
    def show_summary(self, _):

        #--------------------------------------------------
        # Load environment variables
        #--------------------------------------------------

        if getattr(sys, "_MEIPASS", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.getcwd()

        env_path = os.path.join(base_path, ".env")

        os.environ.pop("OPENAI_API_KEY", None) # Because it loads a key from some place I dont know!
        os.environ.pop("TAVILY_API_KEY", None) # Because it loads a key from some place I dont know!
        load_dotenv(env_path) 
        
        #--------------------------------------------------
        # Notify user that summary is being generated
        #--------------------------------------------------

        funny_titles = [
        "😼 Majid – Master of Chaos",
        "🐾 The Overlord Cat",
        "🙀 Guess Who’s Smarter Than You",
        "😹 Your Furry Life Coach",
        "🐈 Professional Napper",
        "🧶 Task Shredder Extraordinaire",
        "🍣 Tuna > Your Deadlines",
        "😾 Stop Bothering Me Human",
        "🐾 The Mighty Meow-nager",
        "😸 Chief of Procrastination"
        ]
        random_title = random.choice(funny_titles)

        pync.notify(
            "Majid is making your summary 🐾",
            title=random_title,
            appIcon=os.path.join(base_path, "icons", "Menu_icon.png"),
            sound="default",
        )

        try:
            summary = self.generate_summary()
            icon_path = os.path.join(base_path, "icons", "App_icon.icns")
            rumps.alert(title="😼 Majid Summary", message=summary, icon_path=icon_path)
        except Exception as e:
            rumps.alert(title="Error", message=f"Failed to generate summary: {str(e)}")
            print(f"Failed to generate summary: {str(e)}")

    #--------------------------------------------------
    # Function to generate summary using LangChain and OpenAI
    #--------------------------------------------------

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
            "1. Start with a sarcastic and hilarious greeting as Majid (short).\n"
            "2. Only use Calendar and list my events for today.\n"
            "3. Only use Reminders that are incomplete or still pending today.\n"
            "4. Only use Notes and use texts that clearly relate to a task that needs to be done. Ignore anything that sounds like a thought, idea, or journal entry.\n"
            "5. Make a clear and organized daily plan, starting with a bullet list of Calendar events, then Reminders, then a short list of tasks based on my Notes (up to 5 max).\n"
            "6. End with a very short and funny summary of what I need to do.\n"
            "7. Keep everything short so that the content fits inside the rump allert window\n\n"

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
    

