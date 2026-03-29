from typing import List


from langchain.messages import AIMessage
from langchain.tools import tool
from langchain_ollama import ChatOllama

@tool("does_user_exits",description="check if user with given user_id exists")
def does_user_exists(user_id:int)->bool:
    return user_id<60

llm=ChatOllama(
    model='llama3',
    temperature=0
).bind_tools([does_user_exists])


result=llm.invoke("check if user with userid 45 exits")
print(result)