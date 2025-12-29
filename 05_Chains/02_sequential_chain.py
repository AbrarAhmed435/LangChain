from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()


template1=PromptTemplate(
    template="Write a report on {topic}",
    input_variables=['topic']
)

template2=PromptTemplate(
    template="Write 4 point about \n {text}",
    input_variables=['text']
)

model=ChatOpenAI(model='gpt-4o-mini')

parser=StrOutputParser()

chain=template1 | model | parser | template2 | model | parser

result=chain.invoke({
    'topic': 'Kashmir'
})



chain.get_graph().print_ascii()

print(result)