from sqlalchemy.orm import Session
from models.tag import Tag
from . import create_item, get_items, get_item_by_id, update_item, delete_item

# 创建Tag
def create_tag(name: str):
    return create_item(Tag, name=name)

# 获取所有Tag
def get_tags():
    return get_items(Tag)

# 根据ID获取Tag
def get_tag_by_id(tag_id: int):
    return get_item_by_id(Tag, tag_id)

# 更新Tag
def update_tag(tag_id: int, **kwargs):
    return update_item( Tag, tag_id, **kwargs)

# 删除Tag
def delete_tag(tag_id: int):
    return delete_item(Tag, tag_id)
