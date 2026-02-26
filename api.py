import os
from dotenv import load_dotenv, find_dotenv
from google import genai

def get_gemini_key():
    _ = load_dotenv(find_dotenv())
    return os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=get_gemini_key()) 

print("Your API Key loaded successfully!")
