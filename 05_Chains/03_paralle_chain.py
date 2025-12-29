from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnableParallel

from dotenv import load_dotenv
load_dotenv()


model1=ChatOpenAI(model='gpt-4o-mini')
model2=ChatGoogleGenerativeAI(model='gemini-2.5-flash')



prompt1=PromptTemplate(
    template="Generate short and simple notes from the following test \n {text}",
    input_variables=['text']
)

prompt2=PromptTemplate(
    template="Generate 5 short question answers from the following text \n {text}"
)


prompt3=PromptTemplate(
    template="Merge the provided notes and quiz into a single document \n Notes:{notes}, Quiz:{quiz}"
)

parser=StrOutputParser()

parallel_chain=RunnableParallel({
    'notes':prompt1 | model1 | parser,
    'quiz':prompt2 | model2 | parser
})

merger_chain=prompt3 | model1 | parser 

final_chain=parallel_chain | merger_chain

text='''Love is one of the most profound and complex emotions humans experience. It goes beyond simple attraction or affection; it is a deep connection that binds people through understanding, care, and commitment. Love can exist in many forms—romantic love, familial love, friendship, and even self-love—and each plays a vital role in shaping who we are.

At its core, love is about empathy and acceptance. It allows us to see another person not as perfect, but as real, with flaws, fears, and dreams. True love does not demand change; instead, it encourages growth while offering a sense of safety and belonging. When we love someone, we invest emotionally, choosing to support them not only in moments of happiness but also during times of struggle.

Love also requires effort and patience. Contrary to popular belief, it is not sustained by intense emotions alone. Over time, love evolves into trust, respect, and shared responsibility. Disagreements and misunderstandings are inevitable, but love teaches us how to communicate, forgive, and compromise. These moments test the strength of the bond and often deepen it.

Beyond personal relationships, love influences how we interact with the world. It fosters kindness, compassion, and a willingness to help others. Love has the power to heal emotional wounds, inspire creativity, and give life a sense of meaning. It motivates people to become better versions of themselves, not out of obligation, but out of care.

In a world often driven by speed and self-interest, love reminds us to slow down and connect. It is not always loud or dramatic; sometimes, love is found in quiet gestures—a listening ear, a shared silence, or unwavering support. Ultimately, love is not just something we feel; it is something we choose to practice every day.

'''

result=final_chain.invoke({
    'text':text
})

print(result)