from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Annotated

from dotenv import load_dotenv

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini',temperature=1.5)

class Quiz(BaseModel):
    question:Annotated[str,Field(description="Question about topic")]
    option_1:Annotated[str,Field(description="option 1")]
    option_2:Annotated[str,Field(description="option 2")]
    option_3:Annotated[str,Field(description="option 3")]
    option_4:Annotated[str,Field(description="option 4")]
    correct_option_number:Annotated[str,Field(description="Correct option id eg., 1,2,3,4")]


parser=PydanticOutputParser(pydantic_object=Quiz)

template=PromptTemplate(
    template="Generate a quiz question on this {topic} \n {format_instructions}",
    input_variables=['topic'],
    partial_variables={'format_instructions':parser.get_format_instructions()}
)

chain=template | model | parser

topic=str(input("Give your topic name"))

while True:
    result=chain.invoke({
        'topic':topic
    })
    # print(result)
    print(f"Question: {result.question}")
    print(f"1.{result.option_1}")
    print(f"2.{result.option_2}")
    print(f"3.{result.option_3}")
    print(f"4.{result.option_4}")

    correct_option=str(input("Enter correct option"))
    if correct_option==result.correct_option_number:
        print("Correct Answer")
    else:
        print(f"Wrong Answer, correct option is {result.correct_option_number}")




