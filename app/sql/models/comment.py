from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.sql.database import Base 

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(Text, nullable=False)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # articleId = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'))
    # article = relationship('Article', back_populates='comments')

    # authorId = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    # author = relationship('User', back_populates='comments')
