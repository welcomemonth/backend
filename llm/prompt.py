from pydantic import BaseModel, Field
from const import PROMPT_PATH
# 创建一个prompt类，用于提供大语言模型提问的输入，它包含prompt模板路径，从文件中读取，以及需要用户的输入
class Prompt(BaseModel):
    template: str = Field(..., description="The path of the prompt template file")
    
    def read_template(self):
        with open(self.template, "r", encoding="utf-8") as f:
            return f.read()
        
    def generate_prompt(self):
        template = self.read_template()
        return template
    
    def __str__(self) -> str:
        return self.generate_prompt()
    
    def __repr__(self):
        return self.generate_prompt()

def get_gen_prd_prompt():
    return Prompt(template=str(PROMPT_PATH / "prd.prompt")).generate_prompt()

if __name__ == "__main__":
    prompt = Prompt(template="./prompt/prd.prompt", user_input="Hello, who are you?")
    print(prompt)


