"""
This files contains all the routesd to all the web pages.
"""
from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from forms import loginForm, createAccountForm, chatForm
import database as db #custum sqlalchemy database
from sqlalchemy import Select
from huggingBot import huggingBot #custom hugging face api

views = Blueprint("views", import_name=__name__)
bcrypt = None
user = None #this user curetnly on the page
bot = huggingBot() #the active hugging face model
chatMessages = []

@views.route("/", methods = ["POST", "GET"])
def home():
    form = chatForm()
    username = "User"
    if user != None:
        username = user.username #if there as an active user, set the user name to that their name
    if form.is_submitted():
        chatMessages.append(f"{username}: {form.chat1.data}") #need ot add username from user database
        botResponse = getBotResponse(form.modelName.data, form.chat3.data, form.chat2.data, username + form.chat1.data)
        chatMessages.append(f"Raven : {botResponse}")
        return redirect(url_for("views.home"))
    return render_template("chat.html", title="Home", chatMessages=chatMessages, form=form, user=user)

@views.route("/about")
def about():
    return render_template("about.html", title="About", user=user)

@views.route("/login", methods = ["POST", "GET"])
def login():
    form = loginForm()
    global user
    if form.is_submitted():
        user = validateUser(form.email.data, form.password.data) #get the user object from the database
        if user != None:
            return redirect(url_for("views.home"))  
        else:
            flash("Bad credentials", category="danger")
            return render_template("login.html", title="Login", form=form, user=user)    
    return render_template("login.html", title="Login", form=form, user=user)

@views.route("/logout")
def logout():
    global user
    user = None
    return redirect(url_for("views.home"))

@views.route("/login/create_account", methods = ["POST", "GET"])
def createAccount():
    form = createAccountForm()
    if form.is_submitted():
        createUser(form.userName.data, form.email.data, form.password.data)
        return redirect(url_for("views.home"))
    return render_template("createAccount.html", title="Create Accunt", form=form, user=user)

@views.route("/profile/<userID>")
def profile(userID):
    #add redirect for if user is not logged into session, redirect to log in page
    return render_template("profile.html", userID = userID, user = user)

@views.route("/staging", methods=["POST", "GET"])
def staging(): #this page is used for tecting new templates
    form = chatForm()
    return render_template("testing.html", title="Staging", form=form, user=user)

#helper methods - most of these should be moved to thier respective forms in morms.py
def validateUser(email:str, password:str) -> db.userDB:
    """
    chek the userDB for the users email. if it exists, get the users password and comepare it to the inputted passwrod.
    if the passwrod works 
    """
    try:
        user = db.session.execute(Select(db.userDB).filter_by(email=email)).scalar_one()
        # if bcrypt.check_password_hash(user.password, password):
        #     return user
        if password == user.password:
            print(f"logged in as: {user.username}")
            return user
    except:
        print("user not found")
        return None

def createUser(username:str, email:str, password:str):
    """
    This function is for adding new users to the datadase.
    Its takes in the basic information: username, email, and password.
    The funtion also add a user id and a pfp. the id is the number of curent users +1 and the initial pfp is the default pfp
    """
    try:#check if account available
        user = db.session.execute(Select(db.userDB).filter_by(email=email)).scalar_one() #this will throw an error is the email does not exist in the database
        print("user already exists")
        flash("user already created: email already associated with account.")
    except:#create and add new user
        #pw_hash = bcrypt.generate_password_hash(password).decode("utf-8") #incrept the password then convert it to utf-8 string
        id = db.session.query(db.userDB).count() + 1 #the id of the new user is number of curent users +1
        #newUser = userDB(id=id, username=username, email=email, password=pw_hash, pfp="defaultPfp.jpg") #passwords should be encrypted but its being buggy rgiht now
        newUser = db.userDB(id=id, username=username, email=email, password=password, pfp="defaultPfp.jpg")
        db.session.add(newUser)
        db.session.commit()
        print("user created successfuly.")
        flash("User created successfuly.", category="info")

def deleteUser(id:int):
    user = db.session.execute(Select(db.userDB).filter_by(id=id)).scalar_one() #get the user based on thier id
    db.session.delete(user)
    db.session.commit()

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




