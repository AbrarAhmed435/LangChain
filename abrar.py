import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv

load_dotenv()

def check_gemini_api_key():
    # The SDK automatically looks for the GEMINI_API_KEY environment variable
    api_key = os.getenv("GOOGLE_API_KEY") 

    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not found.")
        print("Please set the environment variable or pass the key to genai.configure(api_key=...).")
        return

    try:
        # Configure the client with the key (SDK automatically picks up env var)
        genai.configure(api_key=api_key)

        # Try a simple API call, e.g., listing models, to verify the key
        models = genai.list_models()
        print("Success: Gemini API key is valid and connected.")
        # Optional: Print some available models
        # for model in models:
        #     print(f"- {model.name}")

    except Exception as e:
        print(f"Error: The provided Gemini API key is invalid or an issue occurred: {e}")

if __name__ == "__main__":
    check_gemini_api_key()
