from youtube_transcript_api import YouTubeTranscriptApi

video_id = "FB_kOSHk1DM"

ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch(video_id)

print(transcript[0])

# text = " ".join([snippet.text for snippet in transcript])

# print(text)
