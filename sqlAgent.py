from langchain_ollama.chat_models import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from langchain import hub 
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


def get_engine_for_mysql_db():
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "Root"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_DB = "aisec"

    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
        poolclass=NullPool,
    )
    return engine
llm = ChatOllama(
    model="llama3.1",
    temperature=0,
    # other params...
)

# Initialize MySQL database engine
engine = get_engine_for_mysql_db()

# Create an SQLDatabase object for LangChain utilities
db = SQLDatabase(engine)
prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="SQLite", top_k=5)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_react_agent(
    llm, toolkit.get_tools(), state_modifier=system_message
)

example_query = "Which country's customers spent the most?"

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()