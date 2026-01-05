from langchain_community.retrievers import WikipediaRetriever

retriver=WikipediaRetriever(
    top_k_results=2,
    lang='en'
)

query="lakshadweep Islands"

docs=retriver.invoke(query)
print(len(docs))

for i ,doc in enumerate(docs):
    print(f"########################Result {i}######################################")
    print(doc.page_content)