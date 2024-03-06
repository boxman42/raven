"""
This files contains all the routesd to all the web pages.
"""
from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from forms import loginForm, createAccountForm, chatForm

views = Blueprint("views", import_name=__name__)

@views.route("/")
def home():
    form = chatForm()
    return render_template("chat.html", title="Home", form=form)

@views.route("/about")
def about():
    return render_template("about.html", title="About")

@views.route("/login", methods = ["POST", "GET"])
def login():
    form = loginForm()
    if form.is_submitted():
        print(f"user: {form.email.data}, password: {form.password.data}")
        return redirect(url_for("views.home"))
    return render_template("login.html", title="Login", form=form)


@views.route("/login/create_account", methods = ["POST", "GET"])
def createAccount():
    form = createAccountForm()
    if form.is_submitted():
        flash("User created successfuly.", category="info")
        return redirect(url_for("views.home"))
    return render_template("createAccount.html", title="Create Accunt", form=form)

@views.route("/user/<userID>")
def user(userID):
    #add redirect for if user is not logged into session, redirect to log in page
    return render_template("profile.html", userName = userID)