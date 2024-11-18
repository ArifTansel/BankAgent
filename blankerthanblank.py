from langchain.prompts import PromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from langchain import hub 
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
)
# Yeni bir prompt oluştur
sql_decision_prompt = PromptTemplate(
    input_variables=["query"],
    template=(
        "You are an assistant that decides if an SQL query is necessary. "
        "If the query requires information from the database, return 'SQL_QUERY'. "
        "Otherwise, respond with 'NO_SQL_NEEDED'.\n\n"
        "User Query: {query}\n"
    ),
)

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

# Agent'ın SQL gerekliliğini kontrol eden bir fonksiyon
def should_use_sql(llm, query):
    messages=[
        {"role": "system", "content": """You are an assistant that decides if an SQL query is necessary, databases have this tables (users,transformation_logs,Account_info)
         user information : 
            username , user_id , email and password from users table
         account_information :
            user_balance , user_id 
         transformation_logs :
            receiver and sender user_id , tranformed , amount of translated money
          """
         },
        {"role": "user", "content": sql_decision_prompt.format(query=query)},
    ]
    decision = llm.invoke(messages)
    print(decision.content)
    return "SQL_QUERY" in decision.content

example_query = "my name is a can u give me my transformation_logs"

if should_use_sql(llm,example_query):
    engine = get_engine_for_mysql_db()
    db = SQLDatabase(engine)
    prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
    system_message = prompt_template.format(dialect="SQLite", top_k=5)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_react_agent(
        llm, toolkit.get_tools(), state_modifier=system_message
    )
    print("------- sql Agent ---------------------")
    events = agent_executor.stream(
        {"messages": [("user", example_query)]},
        stream_mode="values",
    )
    for event in events:
        event["messages"][-1].pretty_print()

