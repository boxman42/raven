from database import init_db, db_session
from dbModels import userDB

init_db()
newUser = userDB(id=1237, username="noah", email="noahmu@stfx.ca", password="password1234", pfp="pfp.jpg")
db_session.add(newUser)
db_session.commit()
print(userDB.query.all())
db_session.remove()
