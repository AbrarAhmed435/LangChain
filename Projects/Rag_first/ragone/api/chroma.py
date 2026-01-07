from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

embedding=HuggingFaceBgeEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store=Chroma(
    embedding_function=embedding,
    persist_directory="my-chroma",
    collection_name="rag_docs"
)
