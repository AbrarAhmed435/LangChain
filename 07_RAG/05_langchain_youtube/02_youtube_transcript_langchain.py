from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from  dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

embedding=HuggingFaceBgeEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


loader=YoutubeLoader.from_youtube_url(
    # "https://youtu.be/FBFaOin0gmE?si=-uokraXZ0l4XlLjz",
    # "https://youtube.com/shorts/gqJlqdBv1H0?si=Kyy7-0dia9P-3iHU",
    "https://youtu.be/FB_kOSHk1DM?si=PhFX5q6GmYQXBuLu",
    add_video_info=False,
    # language=["hi","en","id"],
    # translation="en",

    transcript_format=TranscriptFormat.CHUNKS,
    chunk_size_seconds=40,
)

docs=loader.load()

# for doc in docs:
#     print(doc)

# print("\n\n".join(map(repr,docs)))

vector_store=Chroma(
    embedding_function=embedding,
    persist_directory='my-chroma',
    collection_name="sample_docs",
)
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str | None:
    parsed = urlparse(url)

    # youtu.be/<id>
    if parsed.netloc in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip("/")

    # youtube.com/watch?v=<id>
    if parsed.path == "/watch":
        return parse_qs(parsed.query).get("v", [None])[0]

    # youtube.com/shorts/<id>
    if parsed.path.startswith("/shorts/"):
        return parsed.path.split("/")[2]

    return None

for doc in docs:
    doc.metadata.update({
        "source":"youtebe",
        "video_id":"FB_kOSHk1DM"
    })
vector_store.add_documents(docs)


info = vector_store.get()
print("Number of embeddings:", len(info["ids"]))


search_results=vector_store.similarity_search_with_score(
    query="Why is this hook usefull?",
    k=3
)


# print(search_results)

response_data=[]
# response_data.append("Why is this hook usefull?")
response_data.append(search_results)

query=f"Based on context what answer the quetion:Why is this hook usefull if context is not provided says i don't know? \n {response_data}"

res=model.invoke(query).content
print(res)

