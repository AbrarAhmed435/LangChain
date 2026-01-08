from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from  dotenv import load_dotenv
from langchain_openai import ChatOpenAI



loader=YoutubeLoader.from_youtube_url(
    "https://youtu.be/FB_kOSHk1DM?si=PhFX5q6GmYQXBuLu",
    add_video_info=False,
    # language=["hi","en","id"],
    # translation="en",
    transcript_format=TranscriptFormat.CHUNKS,
    chunk_size_seconds=40,
)

docs=loader.load()

print(docs[1])
