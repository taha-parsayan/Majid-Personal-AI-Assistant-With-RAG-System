import customtkinter as ctk
from dotenv import load_dotenv, set_key
import os
import webbrowser
from tkinter import PhotoImage

class ChatboxApp(ctk.CTk):
    def __init__(self):
        super().__init__() # Initialize the ctk class

        #-------------------------------------------------
        # Load existing .env
        #------------------------------------------------
        current_path = os.getcwd()
        self.env_path = os.path.join(current_path, ".env")
        load_dotenv(dotenv_path=self.env_path)

        #-------------------------------------------------
        # GUI
        #-------------------------------------------------
        self.geometry("420x300")
        self.title("Set API Keys")

        self.current_dir = os.getcwd()
        icon_png = os.path.join(self.current_dir, "icons", "Menu_icon.png")   
        if os.path.exists(icon_png):
            icon_img = PhotoImage(file=icon_png)
            self.iconphoto(True, icon_img)

        self.setup_ui()

    #-------------------------------------------------
    # UI construction
    #-------------------------------------------------
    def setup_ui(self):
        # OpenAI
        openai_label = ctk.CTkLabel(self, text="Enter your OpenAI API Key:", font=("Segoe UI", 14))
        openai_label.pack(pady=(20, 5))

        self.openai_entry = ctk.CTkEntry(self, width=300, show="*")
        self.openai_entry.pack(pady=5)

        # Tavily
        tavily_label = ctk.CTkLabel(self, text="Enter your Tavily API Key:", font=("Segoe UI", 14))
        tavily_label.pack(pady=(20, 5))

        self.tavily_entry = ctk.CTkEntry(self, width=300, show="*")
        self.tavily_entry.pack(pady=5)

        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=10)
        buttons_frame.pack(pady=15)

        ok_button = ctk.CTkButton(buttons_frame, text="Save Keys", command=self.save_api_keys)
        ok_button.pack(side="left", padx=10)

        links_button = ctk.CTkButton(buttons_frame, text="Get API Keys", command=self.open_api_links)
        links_button.pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 12))
        self.status_label.pack(pady=5)

    #-------------------------------------------------
    # Function to update .env
    #-------------------------------------------------
    def save_api_keys(self):
        openai_key = self.openai_entry.get().strip()
        tavily_key = self.tavily_entry.get().strip()

        saved_any = False

        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
            set_key(self.env_path, "OPENAI_API_KEY", openai_key)
            saved_any = True

        if tavily_key:
            os.environ["TAVILY_API_KEY"] = tavily_key
            set_key(self.env_path, "TAVILY_API_KEY", tavily_key)
            saved_any = True

        if saved_any:
            self.status_label.configure(text="API keys saved!", text_color="green")
        else:
            self.status_label.configure(text="Please enter at least one key.", text_color="red")

    #-------------------------------------------------
    # Function to open signup/docs pages
    #-------------------------------------------------
    def open_api_links(self):
        webbrowser.open("https://platform.openai.com/signup")   # OpenAI signup
        webbrowser.open("https://docs.tavily.com/")             # Tavily docs

        
if __name__ == "__main__":
    app = ChatboxApp()
    app.mainloop()
