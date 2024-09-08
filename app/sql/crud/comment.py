from sqlalchemy.orm import Session
from models.comment import Comment
from . import create_item, get_items, get_item_by_id, update_item, delete_item

# 创建Comment
def create_comment(body: str, articleId: int, authorId: int):
    return create_item(Comment, body=body, articleId=articleId, authorId=authorId)

# 获取所有Comment
def get_comments():
    return get_items(Comment)

# 根据ID获取Comment
def get_comment_by_id(comment_id: int):
    return get_item_by_id(Comment, comment_id)

# 更新Comment
def update_comment(comment_id: int, **kwargs):
    return update_item(Comment, comment_id, **kwargs)

# 删除Comment
def delete_comment(comment_id: int):
    return delete_item(Comment, comment_id)
