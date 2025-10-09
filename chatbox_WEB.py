#--------------------------------------------------
# Include packages
#--------------------------------------------------
import os, sys

print("\nRunning chatbox_WEB with:", sys.executable)
print("Frozen:", getattr(sys, "frozen", False))
print('\n')

from langchain_functions import *
from flask import Flask, request, jsonify
import webbrowser, subprocess
from langchain.schema import AIMessage, HumanMessage
import rumps
import sys
import importlib

print("\nDone\n")

print("\nMaking Flask app...\n")
app = Flask(__name__)
print("\nDone\n")

#--------------------------------------------------
# Chain & chat history
#--------------------------------------------------
print("\nSetting up the APIs...\n")

try:
    chain = create_chain()
    chat_history = load_chat_history_from_database()
except Exception as e:
    rumps.alert("Error", f"Could not create the AI agent:\n {str(e)}")

print("\nDone\n")

#--------------------------------------------------
# HTML template
#--------------------------------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>😼 Majid - Your Cat Assistant</title>
    <style>
        body {
            font-family: Helvetica, sans-serif;
            background-color: #2B2B2B;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        .container {
            width: 600px;
            max-width: 90%;
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            height: 90vh;
            box-sizing: border-box;
        }

        #chat_box {
            flex: 1;
            overflow-y: auto;
            background-color: #2B2B2B;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }

        .message {
            margin: 5px 0;
            padding: 8px 12px;
            border-radius: 10px;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }

        .user {
            background-color: #444;
            color: yellow;
            text-align: right;
        }

        .ai {
            background-color: #333;
            color: white;
            text-align: left;
        }

        #entry_box {
            width: 100%;
            height: 60px;
            padding: 10px;
            border-radius: 10px;
            border: none;
            resize: none;
            background-color: #1E1E1E;
            color: white;
            box-sizing: border-box;
            margin-bottom: 10px;
            overflow-y: auto;
        }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 10px;
            background-color: #FFB347;
            color: black;
            font-weight: bold;
            cursor: pointer;
            align-self: flex-end;
        }

        button:hover {
            background-color: #e6a03c;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Chat with Majid</h2>
        <div id="chat_box"></div>
        <textarea id="entry_box" placeholder="Type a message..."></textarea>
        <button onclick="sendMessage()">🐾 Send</button>
    </div>

    <script>
        async function sendMessage() {
            let text = document.getElementById("entry_box").value.trim();
            if (!text) return;
            appendMessage("user", text);
            document.getElementById("entry_box").value = "";

            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            appendMessage("ai", data.response);
        }

        function escapeHtml(unsafe) {
            return unsafe
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#039;");
        }

        function appendMessage(sender, text) {
            const chatBox = document.getElementById("chat_box");
            const div = document.createElement("div");
            div.className = "message " + sender;
            div.innerHTML = escapeHtml(text);
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        document.getElementById("entry_box").addEventListener("keydown", function(event) {
            if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""

#--------------------------------------------------
# Routes
#--------------------------------------------------
@app.route("/")
def index():
    print("\nDef Index\n")
    return HTML


@app.route("/chat", methods=["POST"])
def chat():
    print("\ndef chat\n")
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"response": ""})

    chat_history.append(HumanMessage(content=user_input))
    save_message_in_database("human", user_input)

    response = process_chat(chain, user_input, chat_history)
    chat_history.append(AIMessage(content=response))
    save_message_in_database("ai", response)

    print("\nDone\n")
    return jsonify({"response": response})


#--------------------------------------------------
# Free the ports
#--------------------------------------------------

def free_port(port):
    try:
        result = subprocess.run(
            ["lsof", "-ti", f"tcp:{port}"],
            capture_output=True,
            text=True
        )
        pid = result.stdout.strip()
        if pid:
            subprocess.run(["kill", "-9", pid])
            print(f"Killed process {pid} using port {port}")
        else:
            print(f"No process found on port {port}")
    except Exception as e:
        print("Error freeing port:", e)

#--------------------------------------------------
# Run server
#--------------------------------------------------
def run_flask():
    # free_port(5006)
    webbrowser.open("http://127.0.0.1:5006")
    app.run(port=5006, debug=False)

# if __name__ == "__main__":
#     try:
#         run_flask()
#     except Exception as e:
#         print(f"Error starting the server:\n{str(e)}")


