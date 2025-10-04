import customtkinter as ctk
from langchain.schema import AIMessage, HumanMessage
from langchain_functions import *
from tkinter import PhotoImage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("600x600")
app.title("😼 Majid - Your Cat Assistant")
app.resizable(True, True)
app.configure(fg_color="#2B2B2B")

current_dir = os.getcwd()
icon_png = os.path.join(current_dir, "icons", "Menu_icon.png")   
if os.path.exists(icon_png):
    icon_img = PhotoImage(file=icon_png)
    app.iconphoto(True, icon_img)

#--------------------------------------------------
# Functions
#--------------------------------------------------
chain = create_chain()
chat_history = load_chat_history_from_database()

def insert_message(sender, text, align="left", color="#444444"):
    chat_box.configure(state="normal")
    tag_name = f"{sender}_{align}"

    # Default colors for Majid or others
    bg_color = "#2B2B2B"
    fg_color = "white"

    # If it's the user (your question), use a blue background
    if sender.lower() in ["you", "user"]:  
        bg_color = "#007BFF"   # nice blue
        fg_color = "white"     # white text on blue

    chat_box.insert("end", f"{sender}: {text}\n", tag_name)

    chat_box.tag_config(
        tag_name,
        justify="left" if align == "left" else "right",
        lmargin1=10 if align == "left" else 50,
        rmargin=10 if align == "right" else 50,
        spacing3=5,
        background=bg_color,
        foreground=fg_color,
    )

    chat_box.insert("end", "\n")
    chat_box.see("end")
    chat_box.configure(state="disabled")


def on_talk_button_click():
    user_input = entry_box.get("1.0", "end").strip()
    if not user_input:
        return " "

    insert_message("You", user_input, align="right", color="#0066CC")

    response = process_chat(chain, user_input, chat_history)
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response))
    save_message_in_database("human", user_input)
    save_message_in_database("ai", response)

    insert_message("Majid", response, align="left", color="#444444")

    entry_box.delete("1.0", "end") 

def on_enter_key(event):
    if event.state & 0x0001:  # Shift+Enter = newline
        return
    on_talk_button_click()
    return "break"

#--------------------------------------------------
# Layout
#--------------------------------------------------
frame1 = ctk.CTkFrame(master=app, corner_radius=15, fg_color="#1E1E1E")
frame1.pack(expand=True, fill="both", padx=10, pady=10)

chat_label = ctk.CTkLabel(frame1, text="Chat with Majid", font=("Segoe UI", 16, "bold"))
chat_label.pack(anchor="w", pady=(5, 2), padx=10)

# Chatbox with scrollbar
chat_frame = ctk.CTkFrame(frame1, fg_color="#2B2B2B", corner_radius=10)
chat_frame.pack(expand=True, fill="both", padx=10, pady=5)

chat_box = ctk.CTkTextbox(chat_frame, wrap="word", font=("Helvetica", 12))
chat_box.pack(expand=True, fill="both", side="left", padx=5, pady=5)
chat_box.configure(state="disabled", fg_color="#2B2B2B")  # main background

# Input area
entry_frame = ctk.CTkFrame(frame1, fg_color="#1E1E1E")
entry_frame.pack(fill="x", padx=10, pady=5)

entry_box = ctk.CTkTextbox(entry_frame, height=70, font=("Helvetica", 12), wrap="word")
entry_box.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)
entry_box.bind("<Return>", on_enter_key)
entry_box.bind("<Shift-Return>", lambda event: None)

button_say = ctk.CTkButton(
    entry_frame,
    text="🐾 Send",
    command=on_talk_button_click,
    fg_color="#FFB347",
    text_color="black",
    font=("Segoe UI", 14, "bold"),
    corner_radius=10
)
button_say.pack(side="right", pady=5)

app.mainloop()
