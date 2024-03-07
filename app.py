from flask import Flask
import views
from datetime import timedelta
from database import init_db, db_session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "4rda8v0ecn477bbf8b7d3d96232037f53168f36c7addc44964e08f52478cb985006a7".encode("utf8") #this is just some random string
app.permanent_session_lifetime = timedelta(days=30) #sessions are saved for n days
app.register_blueprint(views.views, url_prefix="/")
views.bcrypt = Bcrypt(app)

@app.teardown_appcontext
def shutdown_session(exception=None): #end database session when website stops runnings
    db_session.remove()

if __name__ == "__main__":
    init_db() #start the database
    app.run(debug=True, port=8000) #start the site