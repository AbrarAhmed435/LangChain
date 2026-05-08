from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm=HuggingFaceEndpoint(
    # repo_id="HuggingFaceH4/zephyr-7b-beta",
    repo_id="openai/gpt-oss-20b",
    task="text-generation"
)

model=ChatHuggingFace(llm=llm)


prompt="""
You are a clinical decision support assistant.

Analyze the following patient data and provide:
1. Overall condition (stable / moderate / critical)
2. Possible medical concerns or diagnoses
3. Key abnormal parameters and why they matter
4. Recommended next steps (tests, monitoring, urgency level)

Patient Data:
{
  "age": 58,
  "gender": "Male",
  "SpO2": 89,
  "heart_rate": 112,
  "blood_pressure": "150/95",
  "respiratory_rate": 24,
  "temperature": 38.5,
  "symptoms": ["shortness of breath", "chest tightness", "fatigue"]
}

Be concise, medically accurate, and prioritize critical risks.
- Highlight life-threatening risks first
- Use medical thresholds for reasoning
- Avoid hallucinations; say "insufficient data" if unsure
- Output in structured JSON
"""

result=model.invoke(prompt)

print(result.content)