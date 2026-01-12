from langchain_openai import ChatOpenAI
from langchain_core.tools import tool,InjectedToolArg
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Annotated
import json
import smtplib
from email.mime.text import MIMEText
from pydantic import BaseModel, Field
import os

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')
# model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class MailResponse(BaseModel):
    subject:Annotated[str,Field(max_length=100,description="This is the subject of Mail")]
    body:Annotated[str,Field(max_length=500,description="This is body of mail")]


@tool("get_mail_id_from_db",description="Tool that fetches mail id of user from database")
def getMail(name:str)->str:
    try:
        with open("db.json","r") as f:
            data=json.load(f)
        for user in data:
            if user.get("name","").lower()==name.lower():
                return user.get("email")
    except FileNotFoundError:
        print("file not found")
        return ""
    except json.JSONDecodeError:
        print("by")
        return ""
    
def generate_mail():
    structured_model=model.with_structured_output(MailResponse)
    return structured_model.invoke(user_query)

@tool("sending_mail",description="Sending mail to give mail_id")
def sendMail(mail_id:str)->str:
    try:
        sender=os.getenv("EMAIL_SENDER")
        receiver=mail_id
        password =os.getenv("EMAIL_PASSWORD")
        if not sender or not password:
            return "Email Credentials not configured"
        my_mail=generate_mail()
        msg=MIMEText(my_mail.body)
        msg['Subject']=my_mail.subject
        msg['From']=sender
        msg["To"]=receiver
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender,password)
        server.sendmail(sender,receiver,msg.as_string())
        server.quit()
        return "Email send Successfully"
    except smtplib.SMTPException as e:
        return "SMTP error while sending mail"
    
    except Exception as e:
        return "Unknown error while sending mail"

def generate_mail_template():
    structured_model=model.with_structured_output(MailResponse)
    return structured_model.invoke(f"""Write a email template for this intent
        Rules:
            1. User {{name}} as placeholder for name
            2.Do not personalize beyond {{name}}
            Intent:{user_query}
"""
    )
    

@tool("Mail_to_all",description="This tool sends mail to all users that are in database ")
def send_mail_to_all(intent):
    template=generate_mail_template()

    with open('db.json','r') as f:
        data=json.load(f)
    
    for user in data:
        name=user['name']
        receiver=user['email']
        mail_subject=template.subject
        mail_body= template.body.replace("{{name}}", name)
        sender=os.getenv("EMAIL_SENDER")
        password =os.getenv("EMAIL_PASSWORD")
        if not sender or not password:
            return "Sender Credentials not configured"
        my_mail=generate_mail()
        msg=MIMEText(mail_body)
        msg['Subject']=mail_body
        msg['From']=sender
        msg["To"]=receiver
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender,password)
        server.sendmail(sender,receiver,msg.as_string())
        server.quit()
        return "Email send Successfully"
    

llm_with_tools=model.bind_tools([getMail,sendMail,send_mail_to_all])

user_query=input("Write you query here")

messages=[HumanMessage(user_query)]

test_result=llm_with_tools.invoke(messages)

print(test_result.tool_calls[0])
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
    elif tool_call['name']=='Mail_to_all':
        status=send_mail_to_all.invoke(user_query)

        messages.append(
            ToolMessage(
                content=status,
                tool_call_id=tool_call['id']
            )
        )

        

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