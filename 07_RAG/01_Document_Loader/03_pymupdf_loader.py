from langchain_community.document_loaders import PyMuPDFLoader

loader=PyMuPDFLoader('/home/abrar/Desktop/Abrar/LangChain/Documents/brief-on-Hallmarking.pdf')

docs=loader.load()

print(docs[1].page_content)