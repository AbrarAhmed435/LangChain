
from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import ChatOpenAI
import numpy as np

from dotenv import load_dotenv

load_dotenv()

from PyPDF2 import PdfReader

import re

def pdf_to_sentences(pdf_path):
    reader=PdfReader(pdf_path)
    text=""

    for page in reader.pages:
        text+=page.extract_text()+" "

    text=text.replace("\n"," ")

    sentences=re.split(r'(?<=[.!?])\s+',text)

    sentences=[s.strip() for s in sentences if s.strip()]

    return sentences

SOURCE_PDF="/home/abrar/Desktop/Abrar/LangChain/Documents/the-theories-and-fatality-of-bermuda-triangle-52775.pdf"

document=pdf_to_sentences(SOURCE_PDF)
print(len(document))

#print(document[:5])

embedding=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline

#llm1=HuggingFacePipeline.from_model_id(
 #   model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  #  task='text-generation',
   # pipeline_kwargs=dict(
    #    temperature=0.5,
     #   max_new_tokens=1000
#    )
#)
#model=ChatHuggingFace(llm=llm1)


# llm2=HuggingFacePipeline.from_model_id(
#     model_id="HuggingFaceH4/zephyr-7b-beta",
#     task='text-generation',
#     pipeline_kwargs=dict(
#         temperature=0.5,
#         max_new_tokens=1000
#     )
# )
# zephyr=ChatHuggingFace(llm=llm2)


model_2=ChatOpenAI(model='gpt-4o-mini',temperature=0.5)

def generate_embeddings(document):
    if isinstance(document,list):
        return embedding.embed_documents(document)
    else:
        return embedding.embed_query(document)


def calling_llm(question,answer):
    prompt=f'''
you are an (Retrieval Augmented Generation) RAG assistant 
RULES:
- Answer ONLY using the provided context.
- if you don't find context say i don't know
- Do NOT use external knowledge.
- Be concise and factual.
context:{answer}
question:{question}
Give Answer
'''
    result=model_2.invoke(prompt)
    return result.content


doc_emb=generate_embeddings(document)



question = ' what was on board  USS Cyclops (1918) a 542-foot-long Navy cargoship ,that  sank somewhere between Barbados and the Chesapeake Bay'


ques_emb=generate_embeddings(question)

scores=cosine_similarity([ques_emb],doc_emb)[0]
top_k=scores.argsort()[::-1][:12]

Answers=[]

for i in top_k:
    Answers+=[document[i]]
#print(Answers)


print("===LLM ANSWER===")

print(calling_llm(question,Answers))








