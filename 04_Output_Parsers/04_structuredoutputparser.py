from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint,HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from output_parsers import StructuredOutputParser,ResponseSchema


from dotenv import load_dotenv
load_dotenv()

llm=HuggingFaceEndpoint(
    # repo_id="HuggingFaceH4/zephyr-7b-beta",
    # repo_id="google/gemma-2-2b-it",
    # repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    # repo_id="zai-org/GLM-4.7-Flash",
    repo_id="openai/gpt-oss-20b",
    # repo_id="openai/gpt-oss-120b",
    # repo_id="HuggingFaceH4/zephyr-7b-gemma-v0.1",
    # repo_id="lmsys/vicuna-13b-v1.5",
    task="text-generation"
)
model=ChatHuggingFace(llm=llm)




        
schema=[
    ResponseSchema(name='fact_1',description='Fact 1 about topic'),
    ResponseSchema(name='fact_2',description='Fact 2 about topic '),
    ResponseSchema(name='fact_3',description='Fact 3 about topic '),
]


parser=StructuredOutputParser.from_response_schemas(schema)

template=PromptTemplate(
    template='Give 3 fact about {topic} \n {format_instructions}',
    input_variables=['topic'],
    partial_variables={'format_instructions':parser.get_format_instructions()}
)

prompt=template.invoke({
    'topic':'Black Hole'
})

print(prompt)


result=model.invoke(prompt)

final_result=parser.parse(result.content)

print(final_result)