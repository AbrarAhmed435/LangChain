from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

prompt=PromptTemplate(
    template="Generate five intersting facts about {topic}",
    input_variables=['topic']
)

model=ChatOpenAI(model='gpt-4o-mini')


parser=StrOutputParser()

#################################
chain=prompt | model | parser
################################

topic=str(input("Enter topic name "))

result=chain.invoke({
    'topic':topic
})

chain.get_graph().print_ascii()

print(result)