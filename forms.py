"""
This script contains all the form templates to be used in html files.
All feilds require a label. The label is Just the name/string/text associated with that feild on the html page
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from dbModels import userDB

class loginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="password", validators=[DataRequired()])
    rememberMe = BooleanField(label="Remember Me")
    submit = SubmitField(label="Sign In")
    createAccount = SubmitField(label="Create Accont")
    forgotPassword = SubmitField(label="Forgot Password")

    def validate(self, email:str):
        #this is where login should be validated. curently being done in views.py under helper functions
        pass

class createAccountForm(FlaskForm):
    userName = StringField(label="Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    passowrdConfirm = PasswordField(label="Confirm Passowrd", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Create Account")

    def validate(self, email):
        #this is whwere new accounts should be validated. it is curently being done in views.py under helper functions
        pass

class chatForm(FlaskForm):
    chat1 = StringField(label="Message Chat", validators=[DataRequired()]) #the main chat box
    chat2 = StringField(label="Knowledge Base") #secondary chat box for extra information
    chat3 = StringField(label="Instructions") #terterary chat box for extra information
    submit = SubmitField(label="Enter")