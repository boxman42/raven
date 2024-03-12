from database import init_db, db_session
from dbModels import userDB
from sqlalchemy import Select
from huggingBot import huggingBot

def deleteUser(id:int):
    user = db_session.execute(Select(userDB).filter_by(id=id)).scalar_one() #get the user based on thier id
    db_session.delete(user)
    db_session.commit()

init_db()

bot = huggingBot()
bot.readInUtterance('hello. how are you today?')
print(f"bot:{bot.generateResponse()}")

#newUser = userDB(id=1237, username="noah", email="noahmu@stfx.ca", password="password1234", pfp="pfp.jpg")
# db_session.add(newUser)
# db_session.commit()
print(userDB.query.all())
db_session.remove()
