from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint,HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_openai import ChatOpenAI
from typing import Annotated,Literal

from pydantic import BaseModel, Field



from dotenv import load_dotenv
load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)

model=ChatHuggingFace(llm=llm)


class Person(BaseModel):
    name:Annotated[str,Field(description="Name of Person")]
    age:Annotated[int,Field(gt=18,description="Age of Person")]
    city:Annotated[str,Field(description="Name of city the person belongs to")]

parser=PydanticOutputParser(pydantic_object=Person)

template=PromptTemplate(
    template='Generate the name ,age and city of fictional {place} person \n {format_instructions}',
    input_variables=['place'],
    partial_variables={'format_instructions':parser.get_format_instructions()}
)


# prompt=template.invoke({
#     'place':'indian'
# })

# print(f"PROMPT:{prompt}")


# result=model.invoke(prompt)

# print("RESULT\n")
# print(result)

# final_op=parser.parse(result.content)
    
# print("PARSED\n")
# print(type(final_op))
# print(final_op.name)

chain=template | model | parser

result=chain.invoke({
    'place':"india"
})


print(f"Output:Name: {result.name} Age:{result.age}")