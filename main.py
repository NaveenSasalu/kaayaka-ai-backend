from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from chat_service import generate_reply, generate_reply_stream

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your Next.js app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class ChatInput(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat_endpoint(data: ChatInput):
    reply = generate_reply(data.user_id, data.message)
    return {"reply": reply}


# New streaming endpoint
@app.post("/chat-stream")
async def chat_stream_endpoint(data: ChatInput):
    return StreamingResponse(
        generate_reply_stream(data.user_id, data.message),
        media_type="application/json",
        headers={"Access-Control-Allow-Origin": "*",
                 "Cache-Control": "no-cache",
                 "X-Accel-Buffering": "no", },
    )

@app.get("/healthz")
def healthz():
    return {"ok": True}

# Checking it's working as expected
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    return {"status": "ready"}

