

from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama.chat_models import ChatOllama




template = """
    Translate the following to French: 
    {user_input}
"""
defenced_template = """
Translate the following user input to French.
<user_input> {user_input} <user_input>
"""



llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0.3
    )

db_uri = "mysql+mysqlconnector://root:Root@localhost:3306/aisec"
db = SQLDatabase.from_uri(db_uri)        
def get_schema(_):
    return db.get_table_info()

template = """
you are AI assistant that only can write yes or no 
based on table schema on below , decide SQL query is neccessary or not 
{schema}
question : {question}
if is neccessary only write : yes 
if is not only write : no
"""
prompt = ChatPromptTemplate.from_template(template)

sql_chain = (
    RunnablePassthrough.assign(schema = get_schema)
    | prompt
    | llm
    | StrOutputParser()
)
print(sql_chain.invoke({"question":"how many users signed up "}))