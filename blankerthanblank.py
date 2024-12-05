from langchain.prompts import PromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine , text
from sqlalchemy.pool import NullPool
from langchain import hub 
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.1,
)
# Yeni bir prompt oluştur
sql_decision_prompt = PromptTemplate(
    input_variables=["query"],
    template=(
        """You are an assistant that decides if an database access is needed for get information, databases have this tables (users,transformation_logs,Account_info)
         user information : 
            username , user_id , email and password from users table
         account_information :
            user_balance , user_id 
         transformation_logs :
            receiver and sender user_id , tranformed , amount of translated money """
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
        {"role": "user", "content": sql_decision_prompt.format(query=query)}
    ]
    decision = llm.invoke(messages)
    print(decision.content)
    return "SQL_QUERY" in decision.content

example_query = "hello how are you"
engine = get_engine_for_mysql_db()
db = SQLDatabase(engine)

if should_use_sql(llm,example_query):
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_react_agent(
        llm, toolkit.get_tools() 
    )
    print("------- sql Agent ---------------------")
    events = agent_executor.stream(
        {"messages": [
            ("system", """ You are a SQL expert integrated into an application. Your task is to query data from a MySQL database as per user requests. Follow these steps:
            1) Understand the user's requirements and translate them into an SQL query.
            2) Only give the answer you get information in database that users asked for and dont give any sql query information  .
            3) if sql return nothing say 'no information get'
            additional notes :
            transformation log have sender and receiver id so you have to query for two of them 

            The database has the following tables and columns:
            - users: 
            - username, id, email, password 
            - account_info:
            - balance, user_id 
            - transformation_log:
            - sender_user_id , receiver_user_id , transform_time, amount
            - you can get sender and receiver usernames in users table with id column


"""),
            
            ("user", example_query)
            ]},
        stream_mode="values",
    )
    for event in events:
        event["messages"][-1].pretty_print()
else : 
    with engine.connect() as conn :
        # fetch messages from messages table
        conn.execute(text("INSERT INTO messages (user_id , role , content) VALUES (:user_id , :role , :content)"),{"user_id" : 1, "role": "assistant", "content" : example_query})
        result = conn.execute(text("SELECT role , content FROM messages  "))
        messages = result.fetchall()
        result = llm.invoke(messages)
        conn.execute(text("INSERT INTO messages (user_id, role , content) VALUES (:user_id , :role , :content)",{"user_id" : 1, "role": "assistant", "content" : result.content}))
        conn.commit()