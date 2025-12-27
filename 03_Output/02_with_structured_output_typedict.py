from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from typing import TypedDict

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')


class Review(TypedDict):
    sumamry:str
    sentiment:str

structured_model=model.with_structured_output(Review)




review='''The hardware project was a valuable learning experience that helped deepen my understanding of system design, component integration, and real-world constraints. Working hands-on with hardware exposed challenges such as power management, debugging physical connections, and timing issues, which are often abstracted away in software projects. While the project faced limitations in terms of resources and occasional hardware failures, these difficulties encouraged problem-solving, teamwork, and careful planning. Overall, the project was both challenging and rewarding, providing practical insights that will be useful for future hardware–software integrated systems.
'''

result=structured_model.invoke(review)

print(result)