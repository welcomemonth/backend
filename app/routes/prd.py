from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from llm.prompt import get_gen_prd_prompt
from openai import OpenAI
import asyncio
import json
import time
import os

client = OpenAI(base_url="https://openai.bida.ai/v1")

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
# rewrite 接口的请求参数 扩写的文本内容 全部的文本内容 用户的扩写需求
class RewriteRequest(BaseModel):
    stream: bool = False
    content: str = Field(..., description="The content to be rewritten")
    all_content: str = Field(..., description="All the content")
    rewrite_requirement: str = Field(..., description="The requirement of rewriting") 
    


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

# 写一个用AI扩写某一段文本的接口
@router.post("/rewrite")
async def rewrite_text(data: RewriteRequest):
    # 暂时随机生成一段扩写后的文本
    rewrite_prompt = f""" 
    原始文本：{data.content}\n
    
    全部文本：{data.all_content}\n
    
    用户需求：{data.rewrite_requirement}\n
    
    扩写要求:
    1. 扩写的文本要符合这一段文本的主题，不能偏离主题。
    2. 扩写的文本要尽量详细，不能简单罗列。
    3. 扩写的文本要符合用户的需求，不能随意发挥。
    4. 扩写的文本要符合这一段文本的风格，不能突兀。
    5. 只要生成扩写的文本即可，不需要生成其他内容。
    """
    messages = [
        {"role": "system", "content": "你是一个资深的产品经理，下面是用户的需求文档中某一段，你需要根据用户的需求进行扩写。"},
        {"role": "user", "content": rewrite_prompt},
    ]
    model = 'gpt-4o'
    if data.stream:
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
