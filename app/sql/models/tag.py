from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.sql.database import Base 

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    
    # articles = relationship('Article', secondary='article_tags', back_populates='tagList')
