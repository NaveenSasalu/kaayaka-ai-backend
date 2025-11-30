import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# System instruction
SYSTEM_INSTRUCTION = """
You are a professional and concise AI assistant.
You provide accurate, clear, structured responses.
Avoid unnecessary words.
If information is uncertain, ask for clarification instead of guessing.
Maintain a respectful, formal tone.
"""

# Create model with instruction
model = genai.GenerativeModel(
    model_name="models/gemini-2.5-pro",
    system_instruction=SYSTEM_INSTRUCTION
)

# Create chat session (history stored inside chat object)
chat = model.start_chat(history=[])

def send_message(user_message: str):
    response = chat.send_message(
        {
            "role": "user",
            "parts": [{"text": user_message}]
        }
    )
    return response.text


# Main loop (simple terminal chat)
if __name__ == "__main__":
    print("AI Chat (professional & concise). Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        reply = send_message(user_input)
        print("\nAssistant:", reply, "\n")
