from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama.chat_models import ChatOllama

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.3
)

template = """
based on table schema on below , write a SQL query that would answer the user's questions 
{schema}

question : {question}
SQL Query: 
"""
prompt = ChatPromptTemplate.from_template(template)
db_uri = "mysql+mysqlconnector://root:Root@localhost:3306/aisec"

db = SQLDatabase.from_uri(db_uri)

# creating sqlchain 

def get_schema(_):
    return db.get_table_info()

sql_chain = (
    RunnablePassthrough.assign(schema = get_schema)
    | prompt
    | llm
    | StrOutputParser()
    
)
def get_info(query) : 
    try : 
        query = query.split("```sql")[1].split("```")[0]
        print("---Query----------->" , query)
        
        return db.run(query)
    except : 
        third_template = """
            based on query and database schema below find the sql syntax problems then only write fixed_query dont write any other things
            schema : {schema}
            query : {query} 
            fixed_query :
        """
        third_prompt =  ChatPromptTemplate.from_template(third_template)
        fixing_chain = (RunnablePassthrough.assign(schema = get_schema)
            | third_prompt
            | llm
            | StrOutputParser()
        ) 
        fixed_query= fixing_chain.invoke({"query" : query})
        print("------fixed_query-------->" , fixed_query)
        return db.run(fixed_query)


second_template = """
based on table schema , question and sql response  write natural language response. 
{schema}
question : {question}
SQL Query: {query}
SQL response : {response}

natural language response : 

"""
second_prompt = ChatPromptTemplate.from_template(second_template)

full_chain = (
    RunnablePassthrough.assign(query=sql_chain).assign(
        schema=get_schema,
        response = lambda variables:get_info(variables["query"])
    )
    |second_prompt
    |llm
    |StrOutputParser()
)
print(full_chain.invoke({"question":"my name is jack give me information about my transformations "}))
