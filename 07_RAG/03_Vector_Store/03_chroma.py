from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from pprint import pprint

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

loader=PyMuPDFLoader('/home/abrar/Desktop/Abrar/LangChain/Documents/The_Cyclops_Story.pdf')

docs=loader.load()

splitter=CharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20,
    separator=''
)

result1=splitter.split_documents(docs)

vector_store=Chroma(
    embedding_function=embedding,
    persist_directory='my-chroma',
    collection_name="sample_docs"
)

vector_store.add_documents(result1) # Every document is also assigned to each doc

print(f"Length of result1 {len(result1)}")

info = vector_store.get()
print("Number of embeddings:", len(info["ids"]))


# info=vector_store.get(include=['embeddings','documents','metadatas'])
# info=vector_store.get(include=['embeddings',])

# pprint(info)

search_result=vector_store.similarity_search(
    query='What is name of island',
    k=1
)
search_result=vector_store.similarity_search_with_score(
    query='What is name of island',
    k=1,
    # filter={"size","large"}
)

print(type(search_result))

# print(len)


####UPDATED EXITING DOCUMENT

# vector_store.update_document(document_id='docment id of that doc which you wnat to update',document=updated_doc)

#### DELETING DOC

# vector_store.delete(ids=[list of ids to delete])
# vector_store.add_documents(documents=[list of documents])