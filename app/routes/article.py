from fastapi import APIRouter, Depends, HTTPException
from app.schemas.article import ArticleCreate, ArticleResponse, CommentCreate, CommentResponse
from app.models.article import Article, Comment
from app.routes.auth import get_current_user

router = APIRouter()

@router.post("/articles", response_model=ArticleResponse)
async def create_article(article: ArticleCreate, user_id: int = Depends(get_current_user)):
    new_article = Article(title=article.title, description=article.description, body=article.body, author_id=user_id)
    await new_article.save()
    return ArticleResponse(title=article.title, description=article.description, body=article.body, author_id=user_id)

@router.post("/articles/{article_id}/comments", response_model=CommentResponse)
async def add_comment(article_id: int, comment: CommentCreate, user_id: int = Depends(get_current_user)):
    new_comment = Comment(body=comment.body, article_id=article_id, author_id=user_id)
    await new_comment.save()
    return CommentResponse(body=comment.body, article_id=article_id, author_id=user_id)
