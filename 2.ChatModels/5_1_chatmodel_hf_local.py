from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline

llm=HuggingFacePipeline.from_model_id(
    model_id="HuggingFaceH4/zephyr-7b-beta",
    task='text-generation',
    pipeline_kwargs=dict(
        temperature=0.5,
        max_new_tokens=10000
    )
)


model=ChatHuggingFace(llm=llm)

result=model.invoke("Prove mathematically that line joining midpoint of two sides of triangle is parallel to third side")

print(result.content)