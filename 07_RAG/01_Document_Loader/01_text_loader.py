from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

loader=TextLoader('/home/abrar/Desktop/Abrar/LangChain/Documents/X_ray_detailed_report.txt',encoding='utf-8')

docs=loader.load()

print(type(docs)) #list
print(len(docs)) # 1
print(type(docs[0])) #Document
print(docs[0]) 
print(docs[0].page_content) 
print(docs[0].metadata) 

prompt=PromptTemplate(
    template="Write short summary of this text \n {text}",
    input_variables=['text']
)
parser=StrOutputParser()

chain=prompt | model | parser

result=chain.invoke({
    'text':docs[0].page_content
})

print(result)