from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embedding=HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = [
    "The cat slept peacefully on the warm window sill.",
    "A sudden rain shower cooled the busy city streets.",
    "Abrar enjoys reading books while drinking hot coffee.",
    "The programmer fixed the bug late at night.",
    "Birds started singing as the sun rose slowly."
]


#Question="Who fixed the bug?"

result=embedding.embed_documents(documents)

question_doc=[
    "Who fixex the bug?",
    "Who enjoys books",
    "Who sleeps?",
    "Who is singing?",
    "Tell me about water?"
]

question=embedding.embed_documents(question_doc)


for q_text,q_vec in zip(question_doc,question):
    cosine=float('-inf')
    index=-1

    for i, row in enumerate(result):
        x=float(np.dot(row,q_vec)/(np.linalg.norm(q_vec)*np.linalg.norm(row)))

        if x >cosine:
            cosine=x
            index=i
    print(f"Question: {q_text}")
    print(f"Answer: {documents[index]}\n\n")