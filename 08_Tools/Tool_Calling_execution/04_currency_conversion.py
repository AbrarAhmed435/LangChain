from langchain_core.tools import tool,InjectedToolArg
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import requests

load_dotenv()

model = ChatOpenAI(model='gpt-4o-mini', temperature=0)

@tool("Currency_convertor", description="Get the current conversion rate between two currencies")
def get_conversion_factor(base_currency: str, target_currency: str) -> float:
    url = f'https://v6.exchangerate-api.com/v6/579eaae88747e201b90b4623/latest/{base_currency.upper()}'
    res = requests.get(url)
    data = res.json()

    factor = data.get('conversion_rates', {}).get(target_currency.upper())
    return factor

@tool("Convert", description="Multiply source amount by conversion factor")
def convert(source_amount: float, conversion_factor: float) -> float:
    return source_amount * conversion_factor

query = HumanMessage("""I need to convert 900 Indian rupees (INR) to USD. 
Please do this step by step:
1. First find the current conversion rate from INR to USD
2. Then use that rate to convert 900 INR to USD""")

llm_with_tools = model.bind_tools([get_conversion_factor, convert])
messages = [query]

# Step 1: Get first response from LLM (should call Currency_convertor)
result = llm_with_tools.invoke(messages)
print(f"First response has {len(result.tool_calls)} tool calls")
messages.append(result)

# Execute the first tool call (Currency_convertor)
for tool_call in result.tool_calls:
    if tool_call['name'] == 'Currency_convertor':
        # FIX: Pass tool_call['args'] not tool_call itself
        factor = get_conversion_factor.invoke(tool_call['args'])
        print(f"Conversion factor: {factor}")
        
        # Append ToolMessage for the FIRST tool call
        messages.append(ToolMessage(
            content=str(factor),
            tool_call_id=tool_call['id']
        ))

# Step 2: Get second response from LLM (should call Convert)
print("\nGetting second response...")
result2 = llm_with_tools.invoke(messages)
print(f"Second response has {len(result2.tool_calls)} tool calls")
messages.append(result2)

# Execute the second tool call (Convert)
for tool_call in result2.tool_calls:
    if tool_call['name'] == "Convert":
        # FIX: Pass tool_call['args'] not tool_call itself
        output = convert.invoke(tool_call['args'])
        print(f"Converted amount: {output}")
        
        # Append ToolMessage for the SECOND tool call
        messages.append(ToolMessage(
            content=str(output),
            tool_call_id=tool_call['id']
        ))

# Step 3: Get final response
print("\nGetting final response...")
final_result = llm_with_tools.invoke(messages)
print(f"Final answer: {final_result.content}")