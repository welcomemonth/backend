from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
import json
import time
import os

client = OpenAI()

router = APIRouter()

class Message(BaseModel):
    content: str
    role: str = "user"


class ChatRequest(BaseModel):
    messages: list[Message]
    stream: bool = True

@router.post("/prd")
async def create_prd():
    async def content_generator():
        for i in range(10):
            yield f"this is prd create part {i}\n"
            time.sleep(1)  # 模拟延迟

    return StreamingResponse(content_generator(), media_type="text/plain")


@router.post("/chat")
async def chat_handler(chat_request: ChatRequest):

    messages = [{"role": "system", "content": "You are a helpful assistant."}] + chat_request.messages
    # Azure Open AI takes the deployment name as the model name
    model = 'gpt-4o-mini'

    if chat_request.stream:

        async def response_stream():
            chat_coroutine = client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
            )
            for event in chat_coroutine:
                yield json.dumps(event.model_dump(), ensure_ascii=False) + "\n"

        return StreamingResponse(response_stream())
    else:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=False,
        )
        return response.model_dump()