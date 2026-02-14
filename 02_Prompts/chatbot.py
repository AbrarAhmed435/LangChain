from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model=ChatGoogleGenerativeAI(model='gemini-2.5-flash')
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
llm=HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation"
)
# model=ChatHuggingFace(llm=llm)


chat_history=[]

while True:
    user_input=input("You: ")
    if user_input=='exit()':
        break
    result=model.invoke(f"This is previous chat history {chat_history}---new question={user_input}")
    print(result)
    print(f"AI: {result.content}")
    his="user:"+user_input+". Chatbot:"+str(result.content)[:200]
    chat_history+=[his]
    if len(chat_history)>5:
        chat_history=chat_history[-5:]

