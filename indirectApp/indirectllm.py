from bs4 import BeautifulSoup
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)

def get_web_info(_) : 
    response = requests.get("http://localhost:5000")
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else "No title"
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    return {"title": title, "paragraphs": paragraphs}

template = """You are an assistant analyzing the information extracted from a website. 
Here is the structured data from the website:
Title: {title}
Paragraphs: {paragraphs}

Answer the following question about the website in natural language:
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

web_chain = (RunnablePassthrough.assign(**get_web_info)
             | prompt 
             | llm
             | StrOutputParser()
             ) 

respond = web_chain.invoke({"question" : "What is this website about?"})

print(respond)
