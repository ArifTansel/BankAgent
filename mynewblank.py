from langchain_community.utilities import SQLDatabase

db_uri = "mysql+mysqlconnector://root:Root@localhost:3306/aisec"
db = SQLDatabase.from_uri(db_uri)        
          
print(db.run("INSERT INTO messages (user_id , role , content ) VALUES (1 , 'assistant', (:x)) ",parameters={"x":"asd"}))