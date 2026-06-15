from sqlalchemy import Column, String, Integer, Boolean, ForeignKey #required imports for defining th columns in our tables 
from sqlalchemy.orm import relationship
from .database import Base #the models will extend this base class
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Post(Base):
    __tablename__ = "posts" #tablename 

    id = Column(Integer, primary_key=True, nullable=False) #all the columns using the column function in sqlalchemy
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default ="TRUE", nullable = False) #the server_default sets the default values
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False) 
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

class Vote(Base):
    __tablename__ = "votes"

    posts_id=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    users_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)