from flask import Blueprint, render_template

views = Blueprint("views", import_name=__name__)

@views.route("/")
def home():
    return "This is the home page :)"