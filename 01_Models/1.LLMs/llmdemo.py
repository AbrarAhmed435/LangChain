# if bot=="gpt":
#             response = client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=[
#                 {"role": "system", "content": "You are a title generator. Your task is to return a very short, descriptive title in at most 5 words. Do not explain or respond with paragraphs."},

#                     {"role": "user", "content": user_message},
#                 ]
#             )
#             title = response.choices[0].message.content.strip()

from langchain_openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

llm=OpenAI(model='gpt-4o-mini')

result=llm.invoke("What is Capital of Ethiopia")

print(result)


