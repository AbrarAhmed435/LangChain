from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents=[
    "this is sentence 1",
    "this is sentence 2",
    "this is sentence 3",
]

result = embedding.embed_documents(documents)
for row in result:
    print(row[:10],end="\n\n")
