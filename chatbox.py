import customtkinter as ctk
from langchain.schema import AIMessage, HumanMessage
from langchain_functions import *

#--------------------------------------------------
# Page setup
#--------------------------------------------------
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("dark-blue")  

app = ctk.CTk()
app.geometry("500x500")
app.title("Majid")
app.resizable(True, True)   # allow resizing
app.configure(fg_color="#303030")

#--------------------------------------------------
# Functions
#--------------------------------------------------
chain = create_chain()
chat_history = load_chat_history_from_database()

def on_talk_button_click():
    user_input = entry_box.get("1.0", "end").strip()
    if not user_input:
        return " "

    chat_box.configure(state="normal")
    chat_box.insert("end", f"\nYou:\n {user_input}\n")

    response = process_chat(chain, user_input, chat_history)
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response))
    save_message_in_database("human", user_input)
    save_message_in_database("ai", response)

    chat_box.insert("end", f"\nMajid:\n {response}\n")
    chat_box.insert("end", "_" * 44 + "\n")
    chat_box.see("end")
    chat_box.configure(state="disabled")

    entry_box.delete("1.0", "end")

def on_enter_key(event):
    if event.state & 0x0001:  # Shift+Enter = newline
        return
    on_talk_button_click()
    return "break"

#--------------------------------------------------
# Layout
#--------------------------------------------------
frame1 = ctk.CTkFrame(
    master=app,
    corner_radius=10,
    border_width=2,
    border_color="#C6C6C6",
    fg_color="#000000"
)
frame1.pack(expand=True, fill="both", padx=10, pady=10)

chat_label = ctk.CTkLabel(frame1, text="Chat History", font=("Helvetica", 14, "bold"))
chat_label.pack(anchor="w", pady=(5, 2), padx=5)

chat_box = ctk.CTkTextbox(frame1, font=("Helvetica", 12), wrap="word")
chat_box.pack(expand=True, fill="both", padx=5, pady=5)
chat_box.configure(state="disabled")

entry_label = ctk.CTkLabel(frame1, text="Your Question", font=("Helvetica", 14, "bold"))
entry_label.pack(anchor="w", pady=(5, 2), padx=5)

entry_box = ctk.CTkTextbox(frame1, height=70, font=("Helvetica", 12), wrap="word")
entry_box.pack(fill="x", padx=5, pady=(0, 5))
entry_box.bind("<Return>", on_enter_key)
entry_box.bind("<Shift-Return>", lambda event: None)

button_say = ctk.CTkButton(
    frame1,
    text="Meow",
    command=on_talk_button_click,
    fg_color="#F9F9F9",
    text_color="#000000",
    font=("Helvetica", 14, "bold")
)
button_say.pack(fill="x", padx=5, pady=(0, 5))

app.mainloop()
