from flask import Flask, redirect, url_for
from views import views
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "jK7rP2vW9L3oT5iM1".encode("utf8") #this is just some random string
app.permanent_session_lifetime = timedelta(days=30) #sessions are saved for n days
app.register_blueprint(views, url_prefix="/")  



if __name__ == "__main__":
    app.run(debug=True, port=8000)