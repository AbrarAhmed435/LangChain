"""
Pypdf read pdf page by page
25 pages=25 document objects
ie., each page has page_content, meta_data,source
"""
from langchain_community.document_loaders import PyPDFLoader



loader=PyPDFLoader('/home/abrar/Desktop/Abrar/LangChain/Documents/brief-on-Hallmarking.pdf')

docs=loader.load()

print(len(docs)) # length is equal to number of pages
print(docs[1].page_content) 




#https://docs.langchain.com/oss/python/integrations/document_loaders