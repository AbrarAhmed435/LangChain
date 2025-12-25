from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


#chat template
chat_template=ChatPromptTemplate([
    ('system','You are a helpful customer suppport agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{query}')

])

chat_history=[]

#load chat history

with open('/home/abrar/Desktop/Abrar/LangChain/Prompts/chat_history.txt') as f:
    for line in f:
        line=line.strip()
        if line.startswith('User:'):
            chat_history.append(
                HumanMessage(content=line.replace("User:","").strip())
            )
        elif line.startswith("Chatbot:"):
            chat_history.append(
                AIMessage(content=line.replace("Chatbot:","").strip())
            )

print(chat_history)


# prompt=chat_template.invoke({'chat_history':chat_history,'query':'Where is my refund'})

# print("===PROMPT===")

# print(prompt)