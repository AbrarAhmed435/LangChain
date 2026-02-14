from langchain_ollama import ChatOllama

model=ChatOllama(
    model='llama3',
    temperature=0
)

print(model.invoke("Hell how are you").content)