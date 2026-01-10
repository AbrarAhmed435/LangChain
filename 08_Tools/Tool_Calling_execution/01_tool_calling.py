from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

@tool
def multiply(a:int,b:int)-> int:
    """ Given 2 numbers a and b this tool returns their products """
    return a*b

print(multiply.invoke({
    'a':3,
    'b':4
}))

model=ChatOpenAI(model='gpt-4o-mini')

# TOOL BINDING
llm_with_tool=model.bind_tools([multiply])

result=llm_with_tool.invoke("Hi, How are you?")
print(result.content)
print()

result=llm_with_tool.invoke("Can you multiple 3 and 10")
print(result)
print()
pprint(result.tool_calls)

"""
The llm doesn't run the tool, it just suggests the tool and the input arguments. the actual executin is handled by LangChain or by Programmer
"""
