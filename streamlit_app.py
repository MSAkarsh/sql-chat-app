from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import streamlit as st
import os

# Load environment variables (including LangSmith API key)
load_dotenv()

# Configure LangSmith tracing (optional - set LANGCHAIN_TRACING_V2=true and LANGSMITH_API_KEY in .env)
if os.getenv("LANGCHAIN_TRACING_V2") == "true":
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    if not os.getenv("LANGSMITH_API_KEY"):
        st.warning("⚠️ LangSmith tracing enabled but LANGSMITH_API_KEY not set. Set it in .env to enable tracing.")

# Streamlit app that connects to a SQLite database (default) or MySQL if you prefer.
# It uses the LangChain/Groq pipeline you supplied to generate SQL and natural language responses.

DB_DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "data.db")


def init_database_sqlite(path: str) -> SQLDatabase:
    db_uri = f"sqlite:///{path}"
    return SQLDatabase.from_uri(db_uri)


def init_database_mysql(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)


def get_sql_chain(db):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
    <SCHEMA>{schema}</SCHEMA>
    
    Conversation History: {chat_history}
    
    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;
    
    Your turn:
    
    Question: {question}
    SQL Query:
    """
    
    prompt = ChatPromptTemplate.from_template(template)

    # Try to use Groq, fall back to error message if API key not set
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    except Exception:
        raise ValueError("GROQ_API_KEY not set. Please set the environment variable: export GROQ_API_KEY='your-key-here'")

    def get_schema(_):
        return db.get_table_info()

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )


def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(db)

    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""

    prompt = ChatPromptTemplate.from_template(template)

    # Try to use Groq, fall back to error message if API key not set
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    except Exception:
        raise ValueError("GROQ_API_KEY not set. Please set the environment variable: export GROQ_API_KEY='your-key-here'")

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]

load_dotenv()

st.set_page_config(page_title="Chat with DB", page_icon=":speech_balloon:")

st.title("Chat with Akarsh DB")

# Auto-connect to SQLite on startup
if "db" not in st.session_state:
    try:
        st.session_state.db = init_database_sqlite(DB_DEFAULT_PATH)
        st.sidebar.success("✓ Connected to SQLite database")
    except Exception as e:
        st.sidebar.error(f"Failed to auto-connect: {e}")

with st.sidebar:
    st.subheader("Database Settings")
    
    # Show API key setup info
    with st.expander("🔑 API Key Setup"):
        st.markdown("""
        **Groq API Key required** (free tier available)
        
        1. Get your key at [console.groq.com](https://console.groq.com)
        2. Open `.env` file in this folder
        3. Paste your key on the `GROQ_API_KEY=` line
        4. Restart the app
        
        Example:
        ```
        GROQ_API_KEY=gsk_xxxxxxxxxxxxx
        ```
        """)
    
    if st.checkbox("Connect to different database"):
        db_type = st.selectbox("Database type", options=["sqlite", "mysql"], index=0)

        if db_type == "sqlite":
            sqlite_path = st.text_input("SQLite DB path", value=DB_DEFAULT_PATH, key="sqlite_path")
        else:
            st.text_input("Host", value="localhost", key="Host")
            st.text_input("Port", value="3306", key="Port")
            st.text_input("User", value="root", key="User")
            st.text_input("Password", type="password", value="admin", key="Password")
            st.text_input("Database", value="Chinook", key="Database")

        if st.button("Connect"):
            with st.spinner("Connecting to database..."):
                try:
                    if db_type == "sqlite":
                        db = init_database_sqlite(st.session_state.get("sqlite_path", DB_DEFAULT_PATH))
                    else:
                        db = init_database_mysql(
                            st.session_state["User"],
                            st.session_state["Password"],
                            st.session_state["Host"],
                            st.session_state["Port"],
                            st.session_state["Database"],
                        )
                    st.session_state.db = db
                    st.success("Connected to database!")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        if "db" not in st.session_state or st.session_state.db is None:
            st.markdown("Please connect to a database using the sidebar.")
            response = "Please connect to a database."
        else:
            try:
                response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
            except ValueError as ve:
                response = f"⚠️ {str(ve)}"
                st.error(response)
            except Exception as e:
                response = f"Error: {str(e)}"
                st.error(response)
            else:
                st.markdown(response)

    st.session_state.chat_history.append(AIMessage(content=response))
