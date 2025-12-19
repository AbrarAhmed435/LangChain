from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# model=ChatOpenAI(model='gpt-4o-mini',temperature=1.1,max_completion_tokens=10)
model=ChatOpenAI(model='gpt-4o-mini',temperature=0.5)

result=model.invoke("what is capital of mars")

print(result)

print("========")

print(result.content)

# gemini-2.5-flash