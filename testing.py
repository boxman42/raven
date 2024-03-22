from huggingBot import huggingBot
import database as db

# #makeing the chat bot work
# bot = huggingBot()
# bot.readInUtterance('hello. how are you today?')
# print(f"bot:{bot.generateResponse()}")


#database testing
# user1 = db.userDB(1, "Noah", "noahmurrant@gmail.com", "password1234")
# db.session.add(user1)
# db.session.commit()
result = db.session.query(db.userDB).all()
print(result)


