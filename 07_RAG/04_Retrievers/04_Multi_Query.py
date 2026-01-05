from langchain_core.documents import Document
from uuid import uuid4
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import MultiQueryRetriever
from dotenv import load_dotenv

load_dotenv()


from langchain_core.documents import Document

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = [
    Document(
        page_content="Regular exercise improves cardiovascular health and helps maintain a healthy weight.",
        metadata={"topic": "health", "category": "fitness"},
        id=1,
    ),
    Document(
        page_content="Strength training builds muscle mass and increases overall metabolic rate.",
        metadata={"topic": "health", "category": "fitness"},
        id=2,
    ),
    Document(
        page_content="Daily walking for at least 30 minutes can significantly reduce the risk of heart disease.",
        metadata={"topic": "health", "category": "fitness"},
        id=3,
    ),
    Document(
        page_content="A balanced diet combined with regular workouts leads to better long-term fitness outcomes.",
        metadata={"topic": "health", "category": "fitness"},
        id=4,
    ),
    Document(
        page_content="Proper sleep is essential for muscle recovery and overall physical performance.",
        metadata={"topic": "health", "category": "fitness"},
        id=5,
    ),
    Document(
        page_content="The stock market fluctuates daily based on economic indicators and investor sentiment.",
        metadata={"topic": "finance"},
        id=6,
    ),
    Document(
        page_content="Artificial intelligence is transforming software development and automation workflows.",
        metadata={"topic": "technology"},
        id=7,
    ),
    Document(
        page_content="The French Revolution was a major turning point in European history.",
        metadata={"topic": "history"},
        id=8,
    ),
    Document(
        page_content="The James Webb Space Telescope provides unprecedented views of distant galaxies.",
        metadata={"topic": "science"},
        id=9,
    ),
    Document(
        page_content="Cooking traditional dishes helps preserve cultural heritage and family traditions.",
        metadata={"topic": "culture"},
        id=10,
    ),
]


vector_store=FAISS.from_documents(
    documents=documents,
    embedding=embedding
)

multiquery_retriever=MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(search_kwargs={"k":5})
    llm=
)

query="How to improve enery levels and maintanin balance?"

results=multiquery_retriever.invoke(query)

print(results)