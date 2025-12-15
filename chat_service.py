import json
import asyncio

import google.generativeai as genai
from dotenv import load_dotenv
import os
from redis_utils import get_history, save_message


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """
You are a professional and concise AI assistant.
Provide accurate, clear, structured responses.
Avoid unnecessary words.
If unsure, ask for clarification.
Maintain a respectful, formal tone.
"""

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

def generate_reply(user_id: str, user_message: str):
    # Load past messages
    history = get_history(user_id)

    # Prepare current message
    user_obj = {"role": "user", "parts": [{"text": user_message}]}

    # Add user message to Redis
    save_message(user_id, user_obj)

    # Prepare messages to send to Gemini
    messages = history + [user_obj]

    # Ask Gemini
    response = model.generate_content(messages)

    reply_text = response.text

    # Prepare assistant message
    assistant_obj = {"role": "model", "parts": [{"text": reply_text}]}

    # Save assistant message to Redis
    save_message(user_id, assistant_obj)

    return reply_text


async def generate_reply_stream(user_id: str, user_message: str):
    history = get_history(user_id)

    # Save user message
    user_obj = {"role": "user", "parts": [{"text": user_message}]}
    save_message(user_id, user_obj)

    messages = history + [user_obj]

    # Start async streaming call
    response = await model.generate_content_async(
        messages,
        stream=True
    )

    collected_text = ""

    # Async generator
    async for chunk in response:
        token = chunk.text or ""
        collected_text += token

        # JSON Lines (one token per line)
        yield json.dumps({"token": token}) + "\n"

        # Let event loop breathe
        await asyncio.sleep(0)

    # Save final assistant message
    assistant_obj = {"role": "model", "parts": [{"text": collected_text}]}
    save_message(user_id, assistant_obj)
