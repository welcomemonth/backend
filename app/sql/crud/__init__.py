from sqlalchemy.orm import Session

# 创建操作
def create_item(model, db: Session, **kwargs):
    db_item = model(**kwargs)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 查询所有记录
def get_items(model, db: Session):
    return db.query(model).all()

# 根据ID查询记录
def get_item_by_id(model, item_id, db: Session):
    return db.query(model).filter(model.id == item_id).first()

# 更新记录
def update_item(model, item_id, db: Session, **kwargs):
    db_item = db.query(model).filter(model.id == item_id).first()
    if db_item:
        for key, value in kwargs.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

# 删除记录
def delete_item(model, item_id, db: Session):
    db_item = db.query(model).filter(model.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

