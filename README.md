# Majid: Personal AI-Assistant With RAG System
![Static Badge](https://img.shields.io/badge/AI%20Agent-FF0000)
![Static Badge](https://img.shields.io/badge/RAG%20SYSTEM-CC7722)
![Static Badge](https://img.shields.io/badge/Python-8A2BE2)

## Overview
Majid is a cat! But not just any cat—he’s your AI-powered assistant built with LangChain, designed to interact with your macOS environment to make life easier (and funnier). Majid is your clever AI cat—curious, playful, and a little mischievous. He helps with research, organization, and planning, all while keeping his cat-like humor and charm.

## What does Majid do?
As a macOS user, you probably have countless notes in the Notes app, forgotten reminders piling up in the Reminders app, and a calendar full of events and meetings. Often these inputs aren’t aligned, get overlooked, or simply become overwhelming—making it hard to keep track of tasks and daily life.

That’s where Majid the cat steps in. By scanning and combining these sources, Majid helps you stay on top of things by providing:

✅ A daily task list intelligently built from your notes, reminders, and calendar events.

💬 A chatbox where you can talk to Majid—using your personal information combined with live internet knowledge.

📄 Unlimited PDF analysis, letting you upload documents and ask questions directly based on their content.

## What else to know?
Majid combines productivity with personality:

🐾 Reads and retrieves notes from the macOS Notes app

📄 Opens and analyzes PDFs on demand

🌐 Searches the web with Tavily

🔎 Performs vector search with FAISS + OpenAI embeddings

💾 Stores and recalls chat history using SQLite

📅 Keeps track of events with Apple Calendar integration

## How to install?

1. Clone the repositiry into your system:

```bash
https://github.com/taha-parsayan/Majid-Personal-AI-Assistant-With-RAG-System
```

2. Install the reuquirements:

```bash
pip install -r requirements.txt
```

3. Go to the [OpenAI](https://openai.com/) webpage and create an API key.

4. Go to the [Tavily](https://www.tavily.com/) webpage and create an API key.

5. In the software folder in your system, create a file called .env and fill it with your API keys:

OPENAI_API_KEY = ?

TAVILY_API_KEY = ?

# How to use?

Open a terminal, use ```cd``` + the address of Majid's folder to go to that folder. Then run the software with ```python main.py```.

You can see Majid in the top pannel of your macbook!