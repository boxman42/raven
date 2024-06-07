#app.py
from flask import Flask, redirect, url_for
from views import views
from datetime import timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "4rda8v0ecn477bbf8b7d3d96232037f53168f36c7addc44964e08f52478cb985006a7".encode("utf8") #this is just some random string
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.permanent_session_lifetime = timedelta(days=30) #sessions are saved for n days
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)