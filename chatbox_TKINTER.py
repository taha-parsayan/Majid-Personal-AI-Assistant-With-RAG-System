import customtkinter as ctk
from langchain.schema import AIMessage, HumanMessage
from langchain_functions import *
from tkinter import PhotoImage
from dotenv import load_dotenv
import os


class ChatboxApp(ctk.CTk):
    def __init__(self):
        super().__init__() # Initialize the ctk class

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
        # Configure window
        #--------------------------------------------------
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.geometry("600x600")
        self.title("😼 Majid - Your Cat Assistant")
        self.resizable(True, True)
        self.configure(fg_color="#2B2B2B")

        icon_png = os.path.join(base_path, "icons", "Menu_icon.png")
        if os.path.exists(icon_png):
            icon_img = PhotoImage(file=icon_png)
            self.iconphoto(True, icon_img)

        #--------------------------------------------------
        # Chain & chat history
        #--------------------------------------------------
        self.chain = create_chain()
        self.chat_history = load_chat_history_from_database()

        #--------------------------------------------------
        # Layout setup
        #--------------------------------------------------
        self.build_ui()

    #--------------------------------------------------
    # UI construction
    #--------------------------------------------------
    def build_ui(self):
        frame1 = ctk.CTkFrame(master=self, corner_radius=15, fg_color="#1E1E1E")
        frame1.pack(expand=True, fill="both", padx=10, pady=10)

        chat_label = ctk.CTkLabel(frame1, text="Chat with Majid", font=("Segoe UI", 16, "bold"))
        chat_label.pack(anchor="w", pady=(5, 2), padx=10)

        # Chatbox
        chat_frame = ctk.CTkFrame(frame1, fg_color="#2B2B2B", corner_radius=10)
        chat_frame.pack(expand=True, fill="both", padx=10, pady=5)

        self.chat_box = ctk.CTkTextbox(chat_frame, wrap="word", font=("Helvetica", 12))
        self.chat_box.pack(expand=True, fill="both", side="left", padx=5, pady=5)
        self.chat_box.configure(state="disabled", fg_color="#2B2B2B")

        # Entry area
        entry_frame = ctk.CTkFrame(frame1, fg_color="#1E1E1E")
        entry_frame.pack(fill="x", padx=10, pady=5)

        self.entry_box = ctk.CTkTextbox(entry_frame, height=70, font=("Helvetica", 12), wrap="word")
        self.entry_box.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)
        self.entry_box.bind("<Return>", self.on_enter_key)
        self.entry_box.bind("<Shift-Return>", lambda event: None)

        button_say = ctk.CTkButton(
            entry_frame,
            text="🐾 Send",
            command=self.on_talk_button_click,
            fg_color="#FFB347",
            text_color="black",
            font=("Segoe UI", 14, "bold"),
            corner_radius=10
        )
        button_say.pack(side="right", pady=5)

    #--------------------------------------------------
    # Message handling
    #--------------------------------------------------
    def insert_message(self, sender, text, align="left"):
        self.chat_box.configure(state="normal")
        tag_name = f"{sender}_{align}"

        bg_color = "#2B2B2B"
        fg_color = "white"
        if sender.lower() in ["you", "user"]:
            # bg_color = "#007BFF"
            fg_color = "yellow"

        # self.chat_box.insert("end", f"{sender}: {text}\n", tag_name)
        self.chat_box.insert("end", f"{text}\n", tag_name)
        self.chat_box.tag_config(
            tag_name,
            justify="left" if align == "left" else "right",
            # lmargin1=10 if align == "left" else 50,
            # rmargin=10 if align == "right" else 50,
            # spacing3=5,
            background=bg_color,
            foreground=fg_color,
        )
        self.chat_box.insert("end", "\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def on_talk_button_click(self):
        user_input = self.entry_box.get("1.0", "end").strip()
        if not user_input:
            return

        self.insert_message("You", user_input, align="right")

        response = process_chat(self.chain, user_input, self.chat_history)
        self.chat_history.append(HumanMessage(content=user_input))
        self.chat_history.append(AIMessage(content=response))
        save_message_in_database("human", user_input)
        save_message_in_database("ai", response)

        self.insert_message("Majid", response, align="left")
        self.entry_box.delete("1.0", "end")

    def on_enter_key(self, event):
        if event.state & 0x0001:
            return  # Shift+Enter
        self.on_talk_button_click()
        return "break"


if __name__ == "__main__":
    app = ChatboxApp()
    app.mainloop()
