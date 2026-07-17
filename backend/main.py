from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.chatbot import GitaChatbot

app = FastAPI(title="KrishnaGPT API")

# Allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
bot = GitaChatbot()


class ChatRequest(BaseModel):
    message: str


from typing import List, Optional


class Source(BaseModel):
    type: str
    chapter: int
    verse: Optional[int] = None
    topic: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]

@app.get("/")
def home():
    return {"message": "KrishnaGPT API is running 🚀"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = bot.chat(request.message)

    return ChatResponse(
        answer=response["answer"],
        sources=response["sources"],
    )