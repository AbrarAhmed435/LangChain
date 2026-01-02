import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text = """
Artificial intelligence is transforming the way modern applications are built and deployed.
It allows systems to learn from data and improve their performance over time.
Software engineering best practices help teams write clean, maintainable, and scalable code.
Proper testing and documentation reduce bugs and make collaboration easier.
Version control systems enable developers to track changes and work efficiently in teams.
Meanwhile, regular exercise plays an important role in maintaining both physical health and mental well-being.
"""

sentences = [s.strip() for s in text.split(".") if s.strip()]

embeddings = [embedding.embed_query(s) for s in sentences]

chunks = []
start = 0
end = 0
threshold = 0.6

for i in range(len(embeddings) - 1):
    cosine = np.dot(embeddings[i], embeddings[i + 1]) / (
        np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i + 1])
    )

    if cosine < threshold:
        chunk_text = " ".join(sentences[start:end + 1])
        chunks.append(chunk_text)
        start = end + 1
        end = end + 1
    else:
        end += 1


chunks.append(" ".join(sentences[start:end + 1]))

print("Chunks:\n")
for c in chunks:
    print("-", c)
