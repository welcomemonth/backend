from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.sql.database import Base  # 引用Base

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())

    # authorId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    # author = relationship('User', back_populates='articles')
    
    # comments = relationship('Comment', back_populates='article', cascade='all, delete-orphan')
    # tagList = relationship('Tag', secondary='article_tags', back_populates='articles')
