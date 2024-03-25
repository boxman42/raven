"""
The is the database for the raven chatbot website. to use:
import database
add new user: 
expUser = db.userDB(1, "Test", "test@email.com", "password")
db.session.add(expUser)
db.session.commit()
"""

#imports
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#setup
Base = declarative_base()

#database models
class userDB(Base): 
    __tablename__ = 'users'
    id = Column(name="id",  type_=Integer, primary_key=True)
    username = Column(type_=String(20), unique=False, nullable=False)
    email = Column(type_=String, unique=True, nullable=False)
    password = Column(type_=String(60), unique=False, nullable=False)
    pfp = Column(type_=String(20), unique=False, nullable=False) #profile picture
    #data for chatbot
    knowledge = Column(type_=String, unique=False, nullable=True)
    instruction = Column(type_=String, unique= False, nullable=True)

    def __init__(self, id:int=0, username:str="test", email:str="test@email.com", password:str="password1234", pfp:str="pfp.jpg", knowledge:str="", instruction:str = ""):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.pfp = pfp
        #for chatbot. this feilds are left empty in initalization as we dont need this when creating a fresh account. this is a bad way of doing it.
        self.knowledge = knowledge
        self.instruction = instruction

    def __repr__(self) -> str:
        return f"ID: {self.id}, Username: {self.username}, Email: {self.email}"
    
#post setup
engine = create_engine("sqlite:///raven.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()