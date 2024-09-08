from litellm import completion
import os
from pydantic import BaseModel


class LLMConfig(BaseModel):
    name: str
    api_base_key: str | None = None
    api_base_url: str | None = "https://openai.bida.ai/v1"
  
class Message(BaseModel):
    role: str
    content: str


# 对外提供对话接口
def chat(messages: list[Message], config: LLMConfig):
    response = completion(
        model=config.name,
        messages=messages,
        api_base=config.api_base,
        api_key=config.api_key
    )
    return response 


if __name__ == "__main__":
    msg: Message = Message(role="user", content="Hello, who are you?")
    print(msg.dict())

