from langchain_core.tools import tool


@tool
def multiply(a:int,b:int)->int:
    """ Multiply two numbers """
    return a*b

result=multiply.invoke({
    "a":3,
    "b":4
})

print(result)

print(multiply.name)
print(multiply.description)
print(multiply.args)

print()

# LLM sees this 
from pprint import pprint
pprint(multiply.args_schema.model_json_schema())