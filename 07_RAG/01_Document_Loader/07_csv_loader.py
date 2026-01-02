from langchain_community.document_loaders import CSVLoader

# EVERY ROW HAS A DOCUMENT OBJECT

loader=CSVLoader('/home/abrar/Desktop/Abrar/LangChain/Documents/IRIS.csv')

docs=loader.load()

print(len(docs)) # equal to no. of rows

print(docs[0]) # first row