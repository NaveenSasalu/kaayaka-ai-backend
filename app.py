import os
from dotenv import load_dotenv
import google.generativeai as genai 

# Load the environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

#response = model.generate_content("Hello, How are you doing?")
response = model.generate_content("How are you?")

print(response.text)
