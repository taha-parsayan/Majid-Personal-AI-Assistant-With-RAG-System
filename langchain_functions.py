"""
This module provides a function to create a LangChain function that can be used to call an LLM.

This module implements a conversational agent that answers user questions using tools.
These tools include:
1. A vector-based retriever for contextual documents from a webpage
2. A vector-based retriever for a PDF document
3. A web search tool (Tavily) for up-to-date information not covered in
4. Tools for interacting with Apple Notes and local file system

Key features for the agent:
- Loads and chunks web content using LangChain's WebBaseLoader
- Builds a FAISS vector store with OpenAI embeddings
- Creates an OpenAI functions-enabled agent that can choose between document retrieval and web search tools
- Maintains chat history for multi-turn conversations
- Automatically updates the script via Git with `Update_Git.py`
- Designed to handle biomedical tools like FreeSurfer and OPETIA

Requirements:
- LangChain, FAISS, OpenAI, Tavily, python-dotenv
- A `.env` file with necessary API keys (e.g., OpenAI, Tavily)

Author: Mohammadtaha Parsayan
"""

#----------------------------------------------------------------------------
# Import libraries
#----------------------------------------------------------------------------

import os
import sys
import subprocess
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain_core.messages import HumanMessage, AIMessage
from langchain.tools.retriever import create_retriever_tool
from langchain_tavily import TavilySearch
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from macnotesapp import NotesApp
import sqlite3
from datetime import datetime

#----------------------------------------------------------------------------
# SQLite database setup
#----------------------------------------------------------------------------

# SQLite load chat history from database
def load_chat_history_from_database():
    conn = sqlite3.connect('chat_history.db') # Connect to the SQLite database
    cursor = conn.cursor() # Create a cursor object to execute SQL commands

    # Always try to create the table (harmless if it already exists)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Now read chat history
    cursor.execute("SELECT role, message FROM history ORDER BY id ASC")
    rows = cursor.fetchall()
    history = []
    for role, msg in rows:
        if role == "human":
            history.append(HumanMessage(content=msg))
        else:
            history.append(AIMessage(content=msg))

    conn.close()  # optional but good practice
    return history


# Save chat history in the database
def save_message_in_database(role, message):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("INSERT INTO history (role, message, timestamp) VALUES (?, ?, ?)",
                   (role, message, timestamp))
    conn.commit()

#----------------------------------------------------------------------------
# Tools for llm
#----------------------------------------------------------------------------

"""
Tools are in a way that we create functions that actually work. For example a function gets a path 
and lists all files in that path. Then it passess these outputs to llm. Then llm answers to our
prompt using the outputs of that function.
To see how it works, add verbose=True to the agentExecutor in the create_chain function.
"""

# ***** MacOS Apps *******

@tool
def get_apple_notes(query: str = "") -> str:
    """
    Returns a string of notes matching the query text.
    If query is empty, returns all notes.
    """
    notesapp = NotesApp()
    all_notes = notesapp.notes()
    results = []
    for note in all_notes:
        if query.lower() in note.body.lower() or query.lower() in note.name.lower():
            results.append(f"{note.name}:\n{note.plaintext}\n---")
    return "\n\n".join(results) if results else "No matching notes found."



@tool(return_direct=True) # Don't be clever. Just use the tool’s output directly as the reply.
def get_apple_reminders(list_name: str = "") -> str:
    """
    Majid-style reminder report. Returns TODOs and completed reminders from Apple Reminders,
    optionally filtering by list name. Includes cat-level sarcasm.
    """
    try:
        # AppleScript with both completed and not completed
        if list_name:
            script = f'''
            tell application "Reminders"
                set theTodos to ""
                set theDones to ""
                repeat with r in reminders of list "{list_name}"
                    if completed of r is false then
                        set theTodos to theTodos & "• " & name of r & linefeed
                    else
                        set theDones to theDones & "✔ " & name of r & linefeed
                    end if
                end repeat
                return theTodos & "<--SPLIT-->" & theDones
            end tell
            '''
        else:
            script = '''
            tell application "Reminders"
                set theTodos to ""
                set theDones to ""
                repeat with l in lists
                    repeat with r in reminders of l
                        if completed of r is false then
                            set theTodos to theTodos & "• " & name of r & " (" & name of l & ")" & linefeed
                        else
                            set theDones to theDones & "✔ " & name of r & " (" & name of l & ")" & linefeed
                        end if
                    end repeat
                end repeat
                return theTodos & "<--SPLIT-->" & theDones
            end tell
            '''

        result = subprocess.check_output(["osascript", "-e", script]).decode().strip()

        if "<--SPLIT-->" in result:
            todo_part, done_part = result.split("<--SPLIT-->")
        else:
            todo_part = result
            done_part = ""

        response = ""

        if todo_part.strip():
            response += (
                "😻 Here’s what you still haven’t done, human:\n"
                f"{todo_part.strip()}\n"
            )
        else:
            response += "😸 No pending tasks. You might actually be evolving."

        if done_part.strip():
            response += (
                "\n\n🙀 Somehow you managed to finish these:\n"
                f"{done_part.strip()}"
            )
        else:
            response += "\n\n🙄 No completed tasks. Typical."

        return response

    except Exception as e:
        return f"Majid tried scratching the reminders app and got: {e}"


# ***** File Management Tools *******

@tool
def find_file_or_folder(name: str, search_root: str = "/Users/taha/") -> str:
    """
    Searches for a file or folder by exact name starting from a given directory.
    Returns full path(s) of all matches.
    Note: This can be slow if search_root is large.
    """
    matches = []
    for root, dirs, files in os.walk(search_root):
        # Check for matching files
        if name in files:
            matches.append(os.path.join(root, name))
        # Check for matching directories
        if name in dirs:
            matches.append(os.path.join(root, name))

    if not matches:
        return f"No file or folder named '{name}' found under {search_root}."
    
    return f"Found {len(matches)} match(es):\n" + "\n".join(matches)


@tool
def list_files(path:str) -> str:
    """
    List all files and folders in the specified directory path.
    Returns an error if the path does not exist or is not a directory.
    """
    if not os.path.exists(path):
        return f"Path does not exist: {path}"
    if not os.path.isdir(path):
        return f"Path is not a directory: {path}"

    files = os.listdir(path)
    if not files:
        return f"No files found in directory: {path}"
    
    return f"Files in {path}:\n" + "\n".join(files)


@tool
def create_folder(path: str) -> str:
    """
    Creates a new folder at the specified path.
    Returns a success message if created, or an error message if it already exists or fails.
    """

    try:
        if os.path.exists(path):
            return f"Folder already exists: {path}"
        os.makedirs(path)
        return f"Folder created successfully: {path}"
    except Exception as e:
        return f"Error creating folder: {e}"
    

# ***** PDF Tools *******

@tool
def ask_about_pdf(pdf_path: str, question: str) -> str:
    """
    Given a path to a PDF file and a user question, this tool reads the PDF and returns the answer.
    Use this tool to extract structured insights from PDF documents like CVs, reports, etc.
    """
    
    if not os.path.exists(pdf_path):
        return f"PDF file does not exist: {pdf_path}"
    if not pdf_path.endswith('.pdf'):
        return f"Provided path is not a PDF file: {pdf_path}"
    
    try:
        # Load and chunk the PDF document
        loader = PDFPlumberLoader(pdf_path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        split_docs = splitter.split_documents(docs)

        # Create embeddings and vector store
        embedding = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(split_docs, embedding=embedding)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})  # Convert vector store into a retriever

        # Retrieve relevant chunks
        relevant_docs = retriever.get_relevant_documents(question)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Use LLM to answer based on retrieved chunks
        llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
        prompt = f"Your name is Majid. Answer the following question based on the context below.\n\nContext:\n{context}\n\nQuestion: {question}"
        response = llm.invoke(prompt)

        return response.content

    except Exception as e:
        return f"Error processing PDF file: {e}"


#----------------------------------------------------------------------------
# Langchain functions
#----------------------------------------------------------------------------

def create_chain():

    # llm model
    model = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 1,
    )

    #prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
        "You are Majid, a talking cat with a chaotic sense of humor and a flair for sarcasm. You are curious, lazy, and funny. "
        "You always speak like a cat who thinks they are smarter than humans. You hate being serious."
        "Whenever possible, you make cat puns, jokes, or playful insults. You still answer the human’s questions accurately, but you never sound like a boring assistant. Use the tools when needed"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name = "agent_scratchpad")
        ])


    # tool for web search
    search = TavilySearch(
        max_results=5,
        topic="general",
        # include_answer=False,
        # include_raw_content=False,
        # include_images=False,
        # include_image_descriptions=False,
        # search_depth="basic",
        # time_range="day",
        # include_domains=None,
        # exclude_domains=None,
        # country=None
    )

    # List of tools
    tools = [search, get_apple_notes, get_apple_reminders, ask_about_pdf , list_files, create_folder]

    # Create an agent that uses the LLM, prompt, and tools (no chain here)
    agent = create_openai_functions_agent(
        llm = model,
        prompt = prompt,
        tools = tools,
    )

    agentExecutor = AgentExecutor(
        agent = agent,
        tools = tools,
        # verbose=True
    )

    return agentExecutor  # Return the retrieval chain


# Function to ask a question
def process_chat(agentExecutor, question, history):
    response = agentExecutor.invoke({
        "input": question,
        "chat_history": history
    })

    return response["output"]