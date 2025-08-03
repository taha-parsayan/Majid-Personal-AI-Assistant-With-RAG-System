"""
GUI for Majid
Application: Talking to Majid as an AI assistant
"""

#--------------------------------------------------
# Import libraries
#--------------------------------------------------
import customtkinter as ctk
from langchain.schema import AIMessage, HumanMessage
from langchain_functions import *
#--------------------------------------------------
# Page setup
#--------------------------------------------------

ctk.set_appearance_mode("dark")  # Modes: system, light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue, dark-blue, green

app = ctk.CTk()
app.geometry("400x800")
app.title("Majid")
app.resizable(False, False)
app.configure(fg_color="#303030")  # Match background to frame color

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

    # Process response
    response = process_chat(chain, user_input, chat_history)
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response))
    save_message_in_database("human", user_input)
    save_message_in_database("ai", response)

    chat_box.insert("end", f"\nMajid:\n {response}\n")
    chat_box.insert("end", "_" * 44 + "\n")
    chat_box.see("end")  # Auto scroll
    chat_box.configure(state="disabled")

    entry_box.delete("1.0", "end")


def on_enter_key(event):
    # Prevent default newline behavior
    if event.state & 0x0001:  # Shift key is held, allow newline
        return
    on_talk_button_click()
    return "break"  # prevent newline


#--------------------------------------------------
# Tools
#--------------------------------------------------

frame1 = ctk.CTkFrame(
    master=app,
    width=390,
    height=790,
    corner_radius=10,
    border_width=2,
    border_color="#0755F2",
    fg_color="#000000"
)
frame1.place(x=5, y=5)

chat_label = ctk.CTkLabel(master=frame1, text="Chat History", font=("Helvetica", 16, "bold"))
chat_label.place(x=10, y=5)

chat_box = ctk.CTkTextbox(master=frame1, width=370, height=560, font=("Helvetica", 14), wrap="word")
chat_box.place(x=10, y=40)
chat_box.configure(state="disabled")

entry_label = ctk.CTkLabel(master=frame1, text="Your Question", font=("Helvetica", 16, "bold"))
entry_label.place(x=10, y=610)

entry_box = ctk.CTkTextbox(master=frame1, width=370, height=90, font=("Helvetica", 14), wrap="word")
entry_box.place(x=10, y=650)
entry_box.bind("<Return>", on_enter_key) # Bind Enter key to send message
entry_box.bind("<Shift-Return>", lambda event: None)  # Let Shift+Enter create new line


button_say = ctk.CTkButton(master=frame1, text="Meow", command=on_talk_button_click, width=370, fg_color="#0755F2")
button_say.place(x=10, y=750)

app.mainloop()
