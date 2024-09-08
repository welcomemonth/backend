from pydantic import BaseModel

class ArticleCreate(BaseModel):
    title: str
    description: str
    body: str

class ArticleResponse(BaseModel):
    title: str
    description: str
    body: str
    author_id: int

class CommentCreate(BaseModel):
    body: str

class CommentResponse(BaseModel):
    body: str
    article_id: int
    author_id: int
