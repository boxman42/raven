"""
This script contains all the form templates to be used in html files.
All feilds require a label. The label is Just the name/string/text associated with that feild on the html page
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import email_validator

class loginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="password", validators=[DataRequired()])
    rememberMe = BooleanField(label="Remember Me")
    submit = SubmitField(label="Sign In")
    createAccount = SubmitField(label="Create Accont")

class createAccountForm(FlaskForm):
    userName = StringField(label="Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    passowrdConfirm = PasswordField(label="Confirm Passowrd", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Create Account")

class chatForm(FlaskForm):
    chat1 = StringField(label="Message Chat", validators=[DataRequired()]) #the main chat box
    chat2 = StringField(label="Extra info", validators=[DataRequired()]) #secondary chat box for extra information
    chat3 = StringField(label="Extra Info", validators=[DataRequired()]) #terterary chat box for extra information