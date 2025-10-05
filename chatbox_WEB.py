from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
import os, sys, webbrowser
from langchain.schema import AIMessage, HumanMessage
from langchain_functions import (
    create_chain,
    process_chat,
    load_chat_history_from_database,
    save_message_in_database,
)

app = Flask(__name__)

#--------------------------------------------------
# Load environment
#--------------------------------------------------
if getattr(sys, "_MEIPASS", False):
    base_path = sys._MEIPASS
else:
    base_path = os.getcwd()

env_path = os.path.join(base_path, ".env")
os.environ.pop("OPENAI_API_KEY", None)
os.environ.pop("TAVILY_API_KEY", None)
load_dotenv(env_path)

#--------------------------------------------------
# Chain & chat history
#--------------------------------------------------
chain = create_chain()
chat_history = load_chat_history_from_database()

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
    return HTML

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"response": ""})

    chat_history.append(HumanMessage(content=user_input))
    save_message_in_database("human", user_input)

    response = process_chat(chain, user_input, chat_history)
    chat_history.append(AIMessage(content=response))
    save_message_in_database("ai", response)

    return jsonify({"response": response})

#--------------------------------------------------
# Run server
#--------------------------------------------------
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5006")
    app.run(port=5006, debug=False)
