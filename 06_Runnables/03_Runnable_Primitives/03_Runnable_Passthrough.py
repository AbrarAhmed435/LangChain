from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

prompt1=PromptTemplate(
    template="Write a joke about {topic}",
    input_variables=['topic']
)

prompt2=PromptTemplate(
    template="Explain this joke \n {joke}",
    input_variables=['joke']
)

parser=StrOutputParser()


chain=RunnableSequence(prompt1,model,parser)

joke_chain=RunnableParallel({
    'joke':RunnablePassthrough(),
    'explain':RunnableSequence(prompt2,model,parser)
})


final_chain=RunnableSequence(chain,joke_chain)

result=final_chain.invoke({
    'topic':'cricket'
})

print(result)