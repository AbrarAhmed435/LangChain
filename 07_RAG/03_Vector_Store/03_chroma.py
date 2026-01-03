from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

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