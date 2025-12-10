# Akarsh DB - SQL Chat Application

A Streamlit-based chat application that allows natural language querying of the Akarsh SQLite database using AI (Groq LLM).

## Features

- 🤖 Natural language to SQL query generation using Groq's LLM
- 💬 Interactive chat interface with conversation history
- 🗄️ Pre-loaded Akarsh database (music store data)
- 🌐 Network accessible - share with friends on your local network
- 🔄 Auto-starts on system login (macOS)

## Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd sqlite_sqlalchemy_example
```

### 2. Set up Python environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure API Key
Get a free Groq API key from [console.groq.com](https://console.groq.com)

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the application
```bash
streamlit run streamlit_app.py --server.port 9999
```

Or use the convenience script:
```bash
./run.sh
```

## Access the App

- **Local:** http://localhost:9999
- **Network:** http://akarsh.local:9999 (custom hostname)

## Database Schema

The Akarsh database contains music store data with tables for Albums, Artists, Customers, Employees, Genres, Invoices, MediaTypes, Playlists, and Tracks.

## Example Queries

Try asking the chat:
- "Which 3 artists have the most tracks?"
- "List the top 10 selling albums"
- "Show me all customers from Brazil"
- "What are the different music genres?"

## Tech Stack

- **Frontend:** Streamlit
- **Database:** SQLite (Akarsh sample database)
- **ORM:** SQLAlchemy
- **LLM:** Groq (llama-3.3-70b-versatile)
- **Framework:** LangChain

## Original SQLAlchemy Examples

The `src/` folder contains original SQLAlchemy ORM examples:
- `src/db.py` — SQLAlchemy engine, session and base
- `src/models.py` — example `User` and `Post` models
- `src/create_db.py` — create the SQLite database and tables
- `src/example_crud.py` — CRUD demonstration

---

Built with ❤️ by Akarsh Srinivas

The SQLite database will be created as `data.db` in the project root. Add it to `.gitignore` if necessary.
