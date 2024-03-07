from database import Base
from sqlalchemy import Column, Integer, String
from datetime import datetime

class userDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=False, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(60), unique=False, nullable=False)
    pfp = Column(String(20), unique=False, nullable=False) #profile picture

    def __init__(self, id:int=0, username:str="test", email:str="test@email.com", password:str="password1234", pfp:str="pfp.jpg"):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.pfp = pfp

    def __repr__(self) -> str:
        return f"ID: {self.id}, Username: {self.username}, Email: {self.email}"