from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint,HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-genration"
)

model_2=ChatOpenAI(model='gpt-4o-mini')

model=ChatHuggingFace(llm=llm)


template1=PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)

template2=PromptTemplate(
    template="Write a 5 line summary on the following text. \n {text}",
    input_variables=['text']
)

prompt1=template1.invoke({
    'topic':'black hole'
})




result=model_2.invoke(prompt1)

prompt2=template2.invoke({
    'text':result
})

result1=model_2.invoke(prompt2)


print(result1.content)

