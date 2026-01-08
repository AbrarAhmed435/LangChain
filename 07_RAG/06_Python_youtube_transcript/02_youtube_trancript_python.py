
from youtube_transcript_api import YouTubeTranscriptApi
from pprint import pprint

video_id = "FB_kOSHk1DM"
ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch(video_id)

CHUNK_SECONDS = 30

chunks = []
current_chunk = []
chunk_start_time = transcript[0].start

for snippet in transcript:
    if snippet.start - chunk_start_time <= CHUNK_SECONDS:
        current_chunk.append(snippet.text)
    else:
        chunks.append({
            "start": chunk_start_time,
            "end": snippet.start,
            "text": " ".join(current_chunk)
        })
        current_chunk = [snippet.text]
        chunk_start_time = snippet.start

# last chunk
if current_chunk:
    chunks.append({
        "start": chunk_start_time,
        "end": chunk_start_time + CHUNK_SECONDS,
        "text": " ".join(current_chunk)
    })

pprint(chunks[0])
