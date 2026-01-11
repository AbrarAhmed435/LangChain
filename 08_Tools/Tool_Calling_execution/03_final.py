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


query=HumanMessage("Can you multiply 35 with 10")

messages=[query]


result=llm_with_tool.invoke(messages)
messages.append(result)
# print(messages)

tool_result=multiply.invoke(result.tool_calls[0])
messages.append(tool_result)

# print(messages)
final_result=llm_with_tool.invoke(messages)
print(final_result)