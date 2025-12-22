from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline

llm=HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task='text-generation',
    pipeline_kwargs=dict(
        temperature=0.5,
        max_new_tokens=10000
    )
)


model=ChatHuggingFace(llm=llm)

result=model.invoke("Prove mathematically that 0 raised to power 0 has a value, of 1 , and also give a detailed report of how it gives value 1.")

print(result.content)