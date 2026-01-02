from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableBranch,RunnablePassthrough,RunnableLambda

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

prompt1=PromptTemplate(
    template="Write a detailed report on topic {topic}",
    input_variables=['topic']
)

prompt2=PromptTemplate(
    template="Summarize the following text \n {text}",
    input_variables=['text']

)

parser=StrOutputParser()

report_gen_chain=RunnableSequence(prompt1,model,parser)


branch_chain=RunnableBranch(
    (lambda x:len(x.split())>200,RunnableSequence(prompt2,model,parser)),
    (lambda x:len(x.split())<=300,RunnablePassthrough()),
    RunnableLambda(lambda x:"Couldn't find matching length")
)

final_chain=RunnableSequence(report_gen_chain,branch_chain)

result=final_chain.invoke({
    'topic':'X-Rays'
})

print(result)