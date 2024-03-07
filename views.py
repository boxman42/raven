"""
This files contains all the routesd to all the web pages.
"""
from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from forms import loginForm, createAccountForm, chatForm
from database import db_session
from dbModels import userDB
from sqlalchemy import Select

views = Blueprint("views", import_name=__name__)
bcrypt = None

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
        user = validateUser(form.email.data, form.password.data)
        if user != None:
            return redirect(url_for("views.home"))  
        else:
            flash("Bad credentials", category="danger")
            return render_template("login.html", title="Login", form=form)    
    return render_template("login.html", title="Login", form=form)

@views.route("/login/create_account", methods = ["POST", "GET"])
def createAccount():
    form = createAccountForm()
    if form.is_submitted():
        createUser(form.userName.data, form.email.data, form.password.data)
        flash("User created successfuly.", category="info")
        return redirect(url_for("views.home"))
    return render_template("createAccount.html", title="Create Accunt", form=form)

@views.route("/user/<userID>")
def user(userID):
    #add redirect for if user is not logged into session, redirect to log in page
    return render_template("profile.html", userName = userID)

#helper methods
def validateUser(email:str, password:str) -> userDB:
    """
    chek the userDB for the users email. if it exists, get the users password and comepare it to the inputted passwrod.
    if the passwrod works 
    """
    try:
        user = db_session.execute(Select(userDB).filter_by(email=email)).scalar_one()
        print(f"UserDB:{user}")
        if bcrypt.check_password_hash(user.password, password):
            return user
    except:
        return None

def createUser(username:str, email:str, password:str):
    """
    This function is for adding new users to the datadase.
    Its takes in the basic information: username, email, and password.
    The funtion also add a user id and a pfp. the id is the number of curent users +1 and the initial pfp is the default pfp
    """
    try:#check if account available
        user = db_session.execute(Select(userDB).filter_by(email=email)).scalar_one() #this will throw an error is the email does not exist in the database
        flash("user already created: email already associated with account.")
    except:#create and add new user
        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8") #incrept the password then convert it to utf-8 string
        id = db_session.query(userDB).count() + 1 #the id of the new user is number of curent users +1
        newUser = userDB(id=id, username=username, email=email, password=pw_hash, pfp="defaultPfp.jpg")
        db_session.add(newUser)
        db_session.commit()

def deleteUser(id:int):
    user = db_session.execute(Select(userDB).filter_by(id=id)).scalar_one() #get the user based on thier id
    db_session.delete(user)
    db_session.commit()