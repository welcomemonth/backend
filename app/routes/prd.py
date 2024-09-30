from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from llm.prompt import get_gen_prd_prompt
from openai import OpenAI
import asyncio
import json
import time
import os

client = OpenAI()

router = APIRouter(prefix="/prd")

class Message(BaseModel):
    content: str
    role: str = "user"


class ChatRequest(BaseModel):
    messages: list[Message]
    stream: bool = True

# 请求生成接口，需要传递项目名称，项目的简单描述
class PrdRequest(BaseModel):
    project_name: str = Field(..., description="The name of the project")
    project_desc: str = Field(..., description="A detailed description of the project")
    # 定义一个可选的流式输出参数，默认为 True
    stream: bool = True
## ceshmain

@router.post("/generate")
async def generate_handler(prd_request: PrdRequest):
    
    prompt = get_gen_prd_prompt().format(project_name=prd_request.project_name, project_description=prd_request.project_desc)
    messages = [{"role": "system", "content": "你是一个资深的产品经理，根据用户输入的项目名称和简单描述，生成一个详细的需求文档。"}]
    messages.append({"role": "system", "content": prompt})
    model = 'gpt-4o'
    async def response_stream():
        chat_coroutine = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        for event in chat_coroutine:
            yield json.dumps(event.model_dump(), ensure_ascii=False) + "\n"

    return StreamingResponse(response_stream())

@router.post("/chat")
async def chat_handler(chat_request: ChatRequest):

    messages = [{"role": "system", "content": "You are a helpful assistant."}] + chat_request.messages
    # Azure Open AI takes the deployment name as the model name
    model = 'gpt-3.5-turbo'
    
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
    
# 写一个获取推文内容的接口
@router.get("/tweets")
async def get_tweets():
    # 暂时随机生成一篇推文
    tweet = "大家好，欢迎大家来中国杭州"
    # 返回推文内容
    return {"tweet": tweet}
    