from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough,RunnableLambda

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

prompt=PromptTemplate(
    template="Write a joke about {topic}",
    input_variables=['topic']
)

def word_counter(text):
    return len(text.split())

parser=StrOutputParser()

joke_gen_chain=RunnableSequence(prompt,model , parser)


parallel_chain=RunnableParallel({
    'joke':RunnablePassthrough(),
    'word_count':RunnableLambda(word_counter)
})

final_chain=RunnableSequence(joke_gen_chain,parallel_chain)


result=final_chain.invoke({
    'topic':'Football'
})

print(result)