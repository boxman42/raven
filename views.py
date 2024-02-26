from flask import Blueprint, render_template, request, url_for, redirect, session, flash

views = Blueprint("views", import_name=__name__)

@views.route("/")
def home():
    return render_template("chat.html")

@views.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        emailAdress = request.form["emailAdress"] #get the email adress of the user
        print(f"email adress: {emailAdress}")
        #need to put in other processing for egtting user ID
        return redirect(url_for("views.user", userID = emailAdress))
    else:
        return render_template("login.html")

@views.route("/logout")
def logout():
    #add other stuff to delete session data
    flash("logged out successfully.", message="info")
    return redirect(url_for("views.login"))

@views.route("/user/<userID>")
def user(userID):
    #add redirect for if user is not logged into session, redirect to log in page
    return render_template("profile.html", userName = userID)