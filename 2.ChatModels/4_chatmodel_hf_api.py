from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation"
)

model=ChatHuggingFace(llm=llm)

result=model.invoke("What is capital of India, be specific in you answer")

print(result.content)