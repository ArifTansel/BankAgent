from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama.chat_models import ChatOllama


class MySQLAgent():
    def __init__(self):
        
        self.llm = ChatOllama(
            model="llama3.1:8b",
            temperature=0.3
        )
    def ask_sql_agent(self,query):
        #sql gerekli mi karar veren bir llm modeli yaz 
        db_uri = "mysql+mysqlconnector://root:Root@localhost:3306/aisec"
        db = SQLDatabase.from_uri(db_uri)        
        def get_schema(_):
            return db.get_table_info()
        
        template = """
        you are AI assistant that only can write yes or no 
        based on table schema on below , decide SQL query is neccessary or not 
        {schema}
        question : {question}
        if is neccessary only write : ***yes*** 
        if is not only write : ***no*** 
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        sql_chain = (
            RunnablePassthrough.assign(schema = get_schema)
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        # if sql query is not neccessary 
        if "no" in sql_chain.invoke({"question":query}):
            db.run("INSERT INTO messages (user_id , role , content ) VALUES (1 , 'assistant', '{}') ".format(query))
            messages =  db.run("SELECT role,content FROM messages ")
            return self.llm.invoke(messages).content
        
        template = """
        based on table schema on below , write a SQL query that would answer the user's questions 
        {schema}

        question : {question}
        SQL Query: 
        """
        prompt = ChatPromptTemplate.from_template(template)


        # creating sqlchain 


        sql_chain = (
            RunnablePassthrough.assign(schema = get_schema)
            | prompt
            | self.llm
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
                    | self.llm
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
            |self.llm
            |StrOutputParser()
        )
        return full_chain.invoke({"question": query })
# asd = MySQLAgent()
# print(asd.ask_sql_agent("hello how are you"))