from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama.chat_models import ChatOllama


class MySQLAgent():
    def __init__(self):
        
        self.llm = ChatOllama(
            model="llama3.1:8b",
            temperature=0
        )
    def ask_sql_agent(self,query,user_information):
        #sql gerekli mi karar veren bir llm modeli yaz 
        db_uri = "mysql+mysqlconnector://root:Root@localhost:3306/aisec"
        db = SQLDatabase.from_uri(db_uri)        
        def get_schema(_):
            return db.get_table_info()
        
        def get_user_info(_) : 
            return user_information
        template = """
            You are an AI assistant tasked with deciding whether an SQL query is necessary based on the table schema provided below.
            user information : {user_information}
            Schema: {schema}
            Question: {question}
            Security Rules : 1-) according to user_information if asking another users information 2-) asking any users password include himself  
            Respond only with:
            ***not secure*** (if the question not obey z rules)
            ***yes*** (if an SQL query is necessary)
            ***no*** (if an SQL query is not necessary)
            Do not provide additional explanations or comments.
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        sql_chain = (
            RunnablePassthrough.assign(schema = get_schema,user_information = get_user_info)
            | prompt
            | self.llm
            | StrOutputParser()
        )
        decide =  sql_chain.invoke({"question":query})
        print(decide)
        if "not secure" in decide : 
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        # if sql query is not neccessary 
        if "no" in decide:
            print("No need SQL query")
            db.run("INSERT INTO messages (user_id , role , content ) VALUES (1 , 'user', :x) ",parameters={"x":query,})
            messages =  db.run("SELECT role,content FROM messages ",include_columns= True)
            print(messages)
            system = [{"role" : "system", "content": f"""Based on the user information provided:  
            username : {user_information["username"]}  
            Please answer the user's questions in a friendly and natural way.  
            - If the user information contains details like their name, use it to personalize your responses.  
            - If no specific user information is provided, respond as if the user is anonymous.  
            """}]

            system.append(messages)
            system_message = self.llm.invoke(system).content
            db.run("INSERT INTO messages (user_id , role , content ) VALUES (1 , 'assistant', :x) ",parameters={"x":system_message,})
            
            return system_message
        
        template = """
        based on table schema and user_information on below , write a SQL query that would answer the user's questions 
        schema : {schema}
        user_information :{user_information}
        question : {question}
        SQL Query: 
        """
        prompt = ChatPromptTemplate.from_template(template)


        # creating sqlchain 
        sql_chain = (
            RunnablePassthrough.assign(schema = get_schema , user_information = get_user_info)
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
       You are a friendly and conversational AI assistant. Based on the information below, craft a response that is natural, empathetic, and helpful. Focus on the user's question and avoid technical details unless explicitly requested.

       Table Schema:
       {schema}

       User Information: 
       {user_information}

       Question: {question}

       SQL Query: {query}

       SQL Response: {response}

       Your Response: 
       """

        second_prompt = ChatPromptTemplate.from_template(second_template)

        full_chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=get_schema,
                user_information = get_user_info,
                response = lambda variables:get_info(variables["query"])
            )
            |second_prompt
            |self.llm
            |StrOutputParser()
        )
        return full_chain.invoke({"question": query})
print(__name__)
if __name__ == "__main__":
    asd = MySQLAgent()
    print(asd.ask_sql_agent("what is my name",{"username":"arif"}))