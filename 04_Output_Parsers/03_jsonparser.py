from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace,HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id='google/gemma-2-2b-it',
    # repo_id='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
    task="text-generation"
)


model=ChatHuggingFace(llm=llm)

parser=JsonOutputParser()

template=PromptTemplate(
    template="Give me the name,age and city of fictional person\n {format_instruction}",
    input_variables=[],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)

chain = template | model | parser

result=chain.invoke({})

print(result)

# prompt=template.format()

# print(prompt)

# result=model.invoke(prompt)

# print(result.content)

# result=parser.parse(result.content)

# print(type(result))

# print(result)
