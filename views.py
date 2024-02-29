"""
Notes:
Inside a Form in an html file, when a post is made(when a submit button is pressed) names and vlues are added to a dictionary.
The name is the name of the block (i.e. <button class="submit" name="submit" value="login">). The name is used as the key in the dictionary.
the value is the value associated with that name. when trying to access values from inputs and buttons in an html file, use: request.form["name"]
"""
from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from forms import loginForm, createAccountForm

views = Blueprint("views", import_name=__name__)

@views.route("/")
def home():
    return render_template("chat.html")

@views.route("/login", methods = ["POST", "GET"])
def login():
    # if request.method == "POST": #checks is a post was made (if a submit button was pressed)
    #     if request.form["submit"] == "login":
    #         emailAdress = request.form["emailAdress"]
    #         print(f"email adress: {emailAdress}")
    #         #need to put in other processing for egtting user ID
    #         return redirect(url_for("views.user", userID = emailAdress))
    #     if request.form["submit"] == "createAccount":
    #         return redirect(url_for("views.createAccount"))
    # else:
    #     return render_template("login.html")
    form = loginForm()
    return render_template("login.html", title="Login", form=form)


@views.route("/login/create_account", methods = ["POST", "GET"])
def createAccount():
    if request.method == "POST":
        emailAdress = request.form["emailAdress"] #get the email adress of the user
        return redirect(url_for("views.user", userID = emailAdress))
    else:
        return render_template("createAccount.html")

@views.route("/user/<userID>")
def user(userID):
    #add redirect for if user is not logged into session, redirect to log in page
    return render_template("profile.html", userName = userID)