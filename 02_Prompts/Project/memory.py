from langchain_core.messages import HumanMessage, AIMessage

def load_chat_history(file_path):
    history=[]

    with open(file_path) as f:
        for line in f:
            line=line.strip()
            if line.startswith("User:"):
                history.append(
                    HumanMessage(content=line.replace("User:","").strip())
                )
            elif line.startswith("Chatbot:"):
                history.append(
                    AIMessage(content=line.replace("Chatbot:","").strip())
                )
    return history

def trim_history(history,max_turns=5):
    if len(history)>10:
        return history[-2*max_turns]
    else:
        return history