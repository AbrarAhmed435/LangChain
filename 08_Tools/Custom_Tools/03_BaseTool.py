"""
BaseTool is the abstract base class for all tools in LangChain, It defines the core structure and interface thet any tool must follow, whether it's a simple one-liner or a fully customized function
All other tool types like @tool, StructuredTool are built on top of BaseTool
"""

from langchain_core.tools import BaseTool
from typing import Annotated,Type
from pydantic import BaseModel,Field

class MultipleInput(BaseModel):
    a:Annotated[int,Field(required=True,description="The first number to add")]
    b:Annotated[int,Field(required=True,description="The second number to add ")]


class MultiplyTool(BaseTool):
    name:Annotated[str,Field(required=True,description="multiply")]
    description:Annotated[str,Field(required=True,description="Multiply two Numbers")]
    args_schema:Type[BaseModel]=MultipleInput

    def _run(self,a:int,b:int)->int: #name should be _run
        return a*b
    
multiple_tool=MultiplyTool()

result=multiple_tool.invoke({
    'a':3,
    'b':5
})
