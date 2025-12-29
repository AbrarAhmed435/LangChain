from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableBranch,RunnableLambda
from pydantic import BaseModel,Field
from typing import Annotated,Literal
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

sender = "abrarnitsri0@gmail.com"
receiver = "tavaheed_2022bite008@nitsri.ac.in"
# receiver="abrar_2022bite057@nitsri.ac.in"
password = "znor ifqn psaw mfwd "


class Sentiment(BaseModel):
    res:Annotated[Literal['pos','neg'],Field(description="Give Sentiment of feedback eg. pos, neg")]


model=ChatOpenAI(model='gpt-4o-mini')

parser=PydanticOutputParser(pydantic_object=Sentiment)
parser2=StrOutputParser()

prompt1=PromptTemplate(
    template="Give sentiment of the feedback {feedback} \n {format_instructions}",
    input_variables=['feedback'],
    partial_variables={'format_instructions':parser.get_format_instructions()}
)

classifier_chain=prompt1 | model | parser

prompt2=PromptTemplate(
    template="Write mail in respose to this positive feedback \n {feedback} from Abrar position :CEO , company: DAND LLM",
    input_variables=['feedback']
)

prompt3=PromptTemplate(
    template="Write mail in repose to this negative feedback \n {feedback}, from Abrar ul Riyaz(Person who  is sending mail to costumer ,position ceo , company DAND LLM)",
    input_variables=['feedback']
)

branch_chain=RunnableBranch(
   # (condition,chain)
    (lambda x:x.res=='pos',prompt2 | model | parser2),
    (lambda x:x.res=='neg',prompt3 | model | parser2),
    RunnableLambda(lambda x:"could not find sentimment")
)

chain=classifier_chain | branch_chain

result=chain.invoke({
    'feedback':"This is terrible Product"
})


print(result)



msg = MIMEText(result)
msg["Subject"] = "Test Mail"
msg["From"] = sender
msg["To"] = receiver
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender, password)
server.sendmail(sender, receiver, msg.as_string())
server.quit()

print("Email sent successfully")


