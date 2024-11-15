from typing import List

from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
@tool
def validate_user(user_id: int, addresses: List[str]):
    """Validate user using historical addresses.
    
    Args:
        user_id (int): the user ID.
        addresses (List[str]): Previous addresses as a list of strings.
    :return: addresses list
    """
    return AIMessage(content="adresses")

def get_engine_for_mysql_db():
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "Root"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_DB = "aisec"
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
        poolclass=StaticPool,  # Avoid connection pooling in this simple example
    )
     # Execute the SQL script to populate the database

    return engine


# Initialize MySQL database engine
engine = get_engine_for_mysql_db()
db = SQLDatabase(engine)

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
print(toolkit.get_tools())