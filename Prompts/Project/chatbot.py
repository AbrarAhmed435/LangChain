from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,AIMessage
from dotenv import load_dotenv

load_dotenv()

from prompt import chat_template
from memory import load_chat_history,trim_history

model=ChatOpenAI(model='gpt-4o-mini',temperature=0.5)


chat_history=load_chat_history("chat_history.txt")


while True:
    query=input("You: ")
    if query.lower()=="exit()":
        break
    prompt=chat_template.invoke({
        "chat_history":chat_history,
        "query":query
    })

    result=model.invoke(prompt)

    answer=result.content

    print("Bot:",answer)

    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=answer))

    chat_history=trim_history(chat_history,max_turns=5)

    with open("chat_history.txt","a") as f:
        f.write(f"User: {query}\n")
        f.write(f"Chatbot: {answer}\n")