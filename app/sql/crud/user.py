from sqlalchemy.orm import Session
from app.sql.models.user import User
from . import create_item, get_items, get_item_by_id, update_item, delete_item

# 创建User
def create_user(db: Session, email: str, username: str, password: str, image: str = None, bio: str = None, demo: bool = False):
    return create_item(model=User, db=db, email=email, username=username, password=password, image=image, bio=bio, demo=demo)

# 获取所有User
def get_users(db: Session):
    return get_items(db=db, model=User)

# 根据ID获取User
def get_user_by_id(db: Session, user_id: int):
    return get_item_by_id(db=db, model=User, item_id=user_id)

# 根据用户名获取User
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# 根据邮箱获取User
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# 更新User
def update_user(db: Session, user_id: int, **kwargs):
    return update_item(db=db, model=User, item_id=user_id, **kwargs)

# 删除User
def delete_user(db: Session, user_id: int):
    return delete_item(db=db, model=User, item_id=user_id)
