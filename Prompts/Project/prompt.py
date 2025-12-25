from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder



chat_template=ChatPromptTemplate([
    ("system","You are a helpfull customer support agent for an online shopping platform"),
    MessagesPlaceholder(variable_name='chat_history'),
    ("human","{query}")    
])