import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-pro")

#response = model.generate_content("Hello, How are you doing?")
response = model.generate_content("Vachana and Kaayaka")

print(response.text)
