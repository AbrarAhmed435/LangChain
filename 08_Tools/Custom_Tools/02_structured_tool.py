from langchain_core.tools import StructuredTool
from pydantic import BaseModel , Field
from typing import Annotated

class MultipleInput(BaseModel):
    a:Annotated[int,Field(required=True,description="The first number to add")]
    b:Annotated[int,Field(required=True,description="The second number to add ")]


def multiply_func(a:int,b:int)->int:
    return a*b

multiply_tool=StructuredTool.from_function(
    func=multiply_func,
    name="multiply",
    description="Multiply two numbers",
    args_schema=MultipleInput
)

result=multiply_tool.invoke({
    'a':4,
    'b':2
})

print(result)
print(multiply_tool.name)
print(multiply_tool.description)
print(multiply_tool.args)
