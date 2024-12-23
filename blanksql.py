# from sqlalchemy import create_engine
# from sqlalchemy.pool import NullPool
# from sqlalchemy import text
# MYSQL_USER = "root"
# MYSQL_PASSWORD = "Root"
# MYSQL_HOST = "localhost"
# MYSQL_PORT = 3306
# MYSQL_DB = "aisec"

# engine = create_engine(
#     f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}",
#     poolclass=NullPool,
# )
# with engine.connect() as conn :
#     t = text("INSERT INTO messages (user_id , role , content) VALUES (:x ,:y ,:z)")
#     conn.execute(t,{"x" : 1, "y":"assistant", "z" : "merhaba"})
#     conn.commit()
from langchain_ollama import ChatOllama

llm = ChatOllama(
            model="llama3.1:8b",
            temperature=0
        )