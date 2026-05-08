from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint,HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


llm=HuggingFaceEndpoint(
    # repo_id="HuggingFaceH4/zephyr-7b-beta",
    # repo_id="google/gemma-2-2b-it",
    # repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    # repo_id="zai-org/GLM-4.7-Flash",
    repo_id="openai/gpt-oss-20b",
    # repo_id="openai/gpt-oss-120b",
    # repo_id="HuggingFaceH4/zephyr-7b-gemma-v0.1",
    # repo_id="lmsys/vicuna-13b-v1.5",
    task="text-generation"
)
model=ChatHuggingFace(llm=llm)

# model=ChatHuggingFace(llm=llm)

template1=PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)

template2=PromptTemplate(
    template="Write a 5 point summary on the following text. \n {text}",
    input_variables=['text']
)

parser=StrOutputParser()

##############  CHAIN  #######################################
 
chain = template1 | model | parser | template2 | model | parser

##############################################################

result=chain.invoke({
    'topic':'black_hole'
})

print(result)