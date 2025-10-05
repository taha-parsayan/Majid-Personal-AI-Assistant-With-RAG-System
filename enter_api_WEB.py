from flask import Flask, render_template_string, request, redirect, url_for
from dotenv import load_dotenv, set_key
import os
import webbrowser
import threading

app = Flask(__name__)

# Path to .env file
env_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path=env_path)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Set API Keys</title>
    <style>
        body { font-family: Segoe UI, sans-serif; background-color: #121212; color: #e0e0e0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background-color: #1e1e1e; padding: 30px; border-radius: 15px; box-shadow: 0 0 20px rgba(255,255,255,0.1); width: 400px; text-align: center; }
        h2 { color: #00b4d8; }
        input[type="password"], input[type="text"] { width: 90%; padding: 10px; border-radius: 5px; border: none; margin-bottom: 15px; background-color: #2b2b2b; color: white; }
        button { padding: 10px 20px; border: none; border-radius: 5px; background-color: #0078d4; color: white; cursor: pointer; margin: 5px; }
        button:hover { background-color: #005a9e; }
        .message { margin-top: 10px; color: {{ color }}; }
        a { color: #00b4d8; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Set API Keys</h2>
        <form method="POST" action="/">
            <label>OpenAI API Key:</label><br>
            <input type="password" name="openai_key" placeholder="Enter OpenAI API key"><br>
            <label>Tavily API Key:</label><br>
            <input type="password" name="tavily_key" placeholder="Enter Tavily API key"><br>
            <button type="submit">Save Keys</button>
        </form>
        <button onclick="window.open('https://platform.openai.com/signup','_blank')">Get OpenAI Key</button>
        <button onclick="window.open('https://docs.tavily.com/','_blank')">Get Tavily Key</button>
        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message, color = "", "white"
    if request.method == "POST":
        openai_key = request.form.get("openai_key", "").strip()
        tavily_key = request.form.get("tavily_key", "").strip()
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
            message, color = "API keys saved successfully!", "lightgreen"
        else:
            message, color = "Please enter at least one key.", "red"

    return render_template_string(HTML, message=message, color=color)


def run_app():
    app.run(port=5005, debug=False)


if __name__ == "__main__":
    threading.Thread(target=run_app).start()
    webbrowser.open("http://127.0.0.1:5005")
