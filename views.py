"""
This files contains all the routesd to all the web pages.
"""
from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from forms import loginForm, createAccountForm, chatForm
from database import db_session
from dbModels import userDB
from sqlalchemy import Select
from huggingBot import huggingBot

views = Blueprint("views", import_name=__name__)
bcrypt = None
user = None #this user curetnly on the page
bot = huggingBot() #the active hugging face model
chatMessages = []

@views.route("/", methods = ["POST", "GET"])
def home():
    form = chatForm()
    if form.is_submitted():
        chatMessages.append(f"User: {form.chat1.data}") #need ot add username from user database
        botResponse = getBotResponse(form.modelName.data, form.chat3.data, form.chat2.data, form.chat1.data)
        chatMessages.append(f"Raven : {botResponse}")
    return render_template("chat.html", title="Home", chatMessages=chatMessages, form=form)

@views.route("/about")
def about():
    return render_template("about.html", title="About")

@views.route("/login", methods = ["POST", "GET"])
def login():
    form = loginForm()
    if form.is_submitted():
        user = validateUser(form.email.data, form.password.data) #get the user object from the database
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

#helper methods - most of these should be moved to thier respective forms in morms.py
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

def getBotResponse(modelName:str, instruction:str, knowledge:str, utterance:str) -> str:
    #set the paramaters
    #this part realy shouldnt have to be done every time, but i dont have time to make it efficient
    if modelName != None: #this is done so the feild are only updated when information is passed in
        bot.setModel(modelName)
    if knowledge != None:
        bot.setKnowledgeBase(knowledge)
    if instruction != None:
        bot.setInstruction(instruction)
    bot.readInUtterance(utterance)
    return bot.generateResponse()




