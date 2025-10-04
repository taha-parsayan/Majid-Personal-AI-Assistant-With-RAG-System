import customtkinter as ctk
from dotenv import load_dotenv, set_key
import os
import webbrowser
from tkinter import PhotoImage

# Load existing .env
current_path = os.getcwd()
env_path = os.path.join(current_path, ".env")
load_dotenv(dotenv_path=env_path)

#-------------------------------------------------
# Function to update .env
#-------------------------------------------------
def save_api_keys():
    openai_key = openai_entry.get().strip()
    tavily_key = tavily_entry.get().strip()

    saved_any = False

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
        set_key(env_path, "OPENAI_API_KEY", openai_key)
        saved_any = True

    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key
        set_key(env_path, "TAVILY_API_KEY", tavily_key)
        saved_any = True

    if saved_any:
        status_label.configure(text="API keys saved!", text_color="green")
    else:
        status_label.configure(text="Please enter at least one key.", text_color="red")

#-------------------------------------------------
# Function to open signup/docs pages
#-------------------------------------------------
def open_api_links():
    webbrowser.open("https://platform.openai.com/signup")   # OpenAI signup
    webbrowser.open("https://docs.tavily.com/")             # Tavily docs

#-------------------------------------------------
# GUI
#-------------------------------------------------
app = ctk.CTk()
app.geometry("420x250")
app.title("Set API Keys")

current_dir = os.getcwd()
icon_png = os.path.join(current_dir, "icons", "Menu_icon.png")   
if os.path.exists(icon_png):
    icon_img = PhotoImage(file=icon_png)
    app.iconphoto(True, icon_img)

# OpenAI
openai_label = ctk.CTkLabel(app, text="Enter your OpenAI API Key:", font=("Segoe UI", 14))
openai_label.pack(pady=(20, 5))

openai_entry = ctk.CTkEntry(app, width=300, show="*")
openai_entry.pack(pady=5)

# Tavily
tavily_label = ctk.CTkLabel(app, text="Enter your Tavily API Key:", font=("Segoe UI", 14))
tavily_label.pack(pady=(20, 5))

tavily_entry = ctk.CTkEntry(app, width=300, show="*")
tavily_entry.pack(pady=5)

# Buttons
buttons_frame = ctk.CTkFrame(app, fg_color="#1E1E1E", corner_radius=10)
buttons_frame.pack(pady=15)

ok_button = ctk.CTkButton(buttons_frame, text="Save Keys", command=save_api_keys)
ok_button.pack(side="left", padx=10)

links_button = ctk.CTkButton(buttons_frame, text="Get API Keys", command=open_api_links)
links_button.pack(side="left", padx=10)

status_label = ctk.CTkLabel(app, text="", font=("Segoe UI", 12))
status_label.pack(pady=5)

app.mainloop()
