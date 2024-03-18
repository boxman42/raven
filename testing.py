from database import init_db, db_session
from dbModels import userDB
from sqlalchemy import Select
from huggingBot import huggingBot


bot = huggingBot()
bot.readInUtterance('hello. how are you today?')
print(f"bot:{bot.generateResponse()}")
