from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, Session
from app.sql.database import Base 

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    image = Column(String, default="https://api.realworld.io/images/smiley-cyrus.jpeg")
    bio = Column(String)
    demo = Column(Boolean, default=False)
    
    # articles = relationship('Article', back_populates='author', cascade='all, delete-orphan')
    # comments = relationship('Comment', back_populates='author', cascade='all, delete-orphan')

    def save(self, db: Session):
        from app.sql.crud.user import create_user
        return create_user(db=db, email=self.email, username=self.username, password=self.password, image=self.image, bio=self.bio, demo=self.demo)