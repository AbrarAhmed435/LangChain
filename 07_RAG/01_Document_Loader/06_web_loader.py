from langchain_community.document_loaders import WebBaseLoader

loader=WebBaseLoader('https://en.wikipedia.org/wiki/Blog')

docs=loader.load()


print(len(docs[0].page_content))
# print(docs[0].page_content)