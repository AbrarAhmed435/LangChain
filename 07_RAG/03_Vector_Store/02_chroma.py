import chromadb

chroma_client=chromadb.Client()
collection=chroma_client.get_or_create_collection(name="document")




collection.add(
    ids=["id1", "id2","id3"],
    documents=[
        "This is a document about Pineapple",
        "This is a document about oranges",
        "I am a fruit that starts with O and end with s",
    ]
)

from pprint import pprint

results=collection.query(
    query_texts=['I have rough surface'],
    n_results=2
)

pprint(results)
