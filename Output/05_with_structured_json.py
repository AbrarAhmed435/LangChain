from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from typing import TypedDict,Annotated,Optional,Literal

from pydantic import BaseModel,Field

load_dotenv()

model=ChatOpenAI(model='gpt-4o-mini')

json_schema={
  "name": "Review",
  "schema": {
    "type": "object",
    "properties": {
      "key_themes": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "maxItems": 50,
        "description": "Write down all key themes discussed in the review"
      },
      "name": {
        "type": ["string", "null"],
        "description": "Write name of person who gave this review. If not mentioned, return null"
      },
      "summary": {
        "type": "string",
        "maxLength": 2000,
        "description": "Give summary of review"
      },
      "sentiment": {
        "type": "string",
        "enum": ["pos", "neg"],
        "description": "Give sentiment of review"
      },
      "pros": {
        "type": ["array", "null"],
        "items": {
          "type": "string"
        },
        "description": "Give pros if present"
      },
      "cons": {
        "type": ["array", "null"],
        "items": {
          "type": "string"
        },
        "description": "Give cons if present"
      }
    },
    "required": ["key_themes", "name", "summary", "sentiment"],
    "additionalProperties": False
  }
}



structured_model=model.with_structured_output(json_schema)




review='''The hardware project proved to be an intensive and intellectually stimulating experience that significantly expanded my understanding of how theoretical concepts translate into real-world systems. Unlike software-focused work, this project demanded close attention to physical constraints such as power consumption, signal integrity, component compatibility, and timing synchronization. Throughout the development process, frequent hardware-related issues—ranging from unstable connections and sensor inaccuracies to unexpected component behavior—required systematic debugging and iterative testing, reinforcing the importance of patience and precision.

Resource limitations and occasional hardware failures initially slowed progress; however, these challenges ultimately strengthened problem-solving skills and encouraged more thoughtful design decisions. The project also highlighted the critical role of documentation, planning, and collaboration, as even small oversights in wiring or configuration could propagate into larger system-level failures. Coordinating between hardware setup and software control logic further emphasized the need for clear interfaces and robust error handling.

Overall, while the project was demanding and at times frustrating, it was highly rewarding. It provided valuable exposure to the complexities of hardware–software integration and offered practical insights that extend beyond academic theory. The experience has fostered a deeper appreciation for embedded systems and has better prepared me for future projects involving real-world engineering constraints, interdisciplinary teamwork, and end-to-end system design.

Review by "Jefferey Epstein"

'''

result=structured_model.invoke(review)

print(result['name'])