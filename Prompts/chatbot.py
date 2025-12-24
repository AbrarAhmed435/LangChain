from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini',temperature=0.5)

chat_history=[]

while True:
    user_input=input("You: ")
    if user_input=='exit()':
        break
    result=model.invoke(f"This is previous chat history {chat_history}---new question={user_input}")
    his="user:"+user_input+". Chatbot:"+str(result.content)
    chat_history+=[his]
    if len(chat_history)>5:
        chat_history=chat_history[-5:]
    print(f"AI: {result.content}")