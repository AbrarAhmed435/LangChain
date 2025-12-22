import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

v1 = embedding.embed_query("I Love this place")
v2 = embedding.embed_query("Light has dual nature")

cosine = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
print(cosine)
