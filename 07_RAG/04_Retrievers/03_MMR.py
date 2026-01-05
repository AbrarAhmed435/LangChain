from uuid import uuid4
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


from langchain_core.documents import Document

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# vector_store=Chroma(
#     embedding_function=embedding,
#     persist_directory='my-chroma',
#     collection_name='sample_docs'
# )


document_1 = Document(
    page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"},
    id=1,
)

document_2 = Document(
    page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
    metadata={"source": "news"},
    id=2,
)

document_3 = Document(
    page_content="Building an exciting new project with LangChain - come check it out!",
    metadata={"source": "tweet"},
    id=3,
)

document_4 = Document(
    page_content="Robbers broke into the city bank and stole $1 million in cash.",
    metadata={"source": "news"},
    id=4,
)

document_5 = Document(
    page_content="Wow! That was an amazing movie. I can't wait to see it again.",
    metadata={"source": "tweet"},
    id=5,
)

document_6 = Document(
    page_content="Is the new iPhone worth the price? Read this review to find out.",
    metadata={"source": "website"},
    id=6,
)

document_7 = Document(
    page_content="The top 10 soccer players in the world right now.",
    metadata={"source": "website"},
    id=7,
)

document_8 = Document(
    page_content="LangGraph is the best framework for building stateful, agentic applications!",
    metadata={"source": "tweet"},
    id=8,
)

document_9 = Document(
    page_content="The stock market is down 500 points today due to fears of a recession.",
    metadata={"source": "news"},
    id=9,
)

document_10 = Document(
    page_content="I have a bad feeling I am going to get deleted :(",
    metadata={"source": "tweet"},
    id=10,
)
document_11 = Document(
    page_content="Eat Healthy food",
    metadata={"source": "tweet"},
    id=11,
)

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10,
    document_11
]

vector_store=FAISS.from_documents(
    documents=documents,
    embedding=embedding
)

# import os
# if not os.path.exists('faiss_db'):
#     vector_store.save_local("faiss_db")

retreiver=vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k":2,"lambda_mult":0.2},
    )
##### range of lambda_mult is [0,1] 0->completerly diffrenet result, 1-> include similar results , 


query="chocolate chip pancakes and scrambled eggs"
results=retreiver.invoke(query)

for r in results:
    print(r.page_content)