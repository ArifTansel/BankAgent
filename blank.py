from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2")

for chunk in llm.stream("can u user langchain tools "):
    print(chunk,end="")