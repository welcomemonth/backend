from sqlalchemy.orm import Session
from app.sql.models.article import Article
from . import create_item, get_items, get_item_by_id, update_item, delete_item

# 创建Article
def create_article(slug: str, title: str, description: str, body: str, authorId: int):
    return create_item(Article, slug=slug, title=title, description=description, body=body, authorId=authorId)

# 获取所有Article
def get_articles():
    return get_items(Article)

# 根据ID获取Article
def get_article_by_id(article_id: int):
    return get_item_by_id(Article, article_id)

# 更新Article
def update_article(article_id: int, **kwargs):
    return update_item(article_id, **kwargs)

# 删除Article
def delete_article(article_id: int):
    return delete_item(Article, article_id)
