from langchain_openai import ChatOpenAI
from langchain_core.tools import tool,InjectedToolArg
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Annotated
import json

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')
# model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

@tool("get_mail_id_from_db",description="Tool that fetches mail id of user from database")
def getMail(name:str)->str:
    with open('db.json','r') as f:
        data=json.load(f)
    email=None
    for user in data:
        if user['name'].lower()==name.lower():
            email=user['email']
    return email

@tool("sending_mail",description="Sending mail to give mail_id")
def sendMail(mail_id:str)->str:
    import smtplib
    from email.mime.text import MIMEText
    sender="abrarnitsri0@gmail.com"
    receiver=mail_id
    password = "znor ifqn psaw mfwd "
    msg=MIMEText("This is a Automated email, send by AI Agent")
    msg['Subject']="Test Mail"
    msg['From']=sender
    msg["To"]=receiver
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender,receiver,msg.as_string())
    server.quit()
    return True


llm_with_tools=model.bind_tools([getMail,sendMail])

messages=[HumanMessage("Send a Mail to Tawheed Tariq , inviting him to party tomorrow")]

test_result=llm_with_tools.invoke(messages)

print(test_result.tool_calls[0]['name'])
messages.append(test_result)

for tool_call in test_result.tool_calls:
    if tool_call['name']=='get_mail_id_from_db':
        email=getMail.invoke(tool_call['args'])
       
        messages.append(
            ToolMessage(
                content=str(email) if email else "Email not found",
                tool_call_id=tool_call['id']
            )
        )
        # else:
        #     error=["Email id not found in database"]
        #     messages.append(error)

result=llm_with_tools.invoke(messages)
messages.append(result)

for tool_call in result.tool_calls:
    if tool_call['name']=='sending_mail':
        status=sendMail.invoke(tool_call['args'])

        messages.append(
            ToolMessage(
                content="Mail send" if status else "Failed to send Mail",
                tool_call_id=tool_call['id']
            )
        )


result=llm_with_tools.invoke(messages)
print(result)

# mail=getMail.invoke(test_result.tool_calls[0])
# print(mail)