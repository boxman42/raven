# Raven RNN ChatBot

## Overview

This is a chatbot website that allows uers to use and customize different chatbots, including hugging face models, RNN models (Raven being currently hosted)

## How to use

download all files then run app.py. you must have flask, flask-wtf, sqlalchemy, and transfomrers installed for everything to run. 

## website

The website is a web interface for the chatbot, similar to chatgpt. The backend uses python and flask, using sqlalchemy for for the database. The front end is primarily html, using bootstrap code blocks for styling.

### Home Page

The home page is were the user interacts with the chatbot. There are three fields for text input: chat1 (main chat box), chat2 (knowledge base), chat3 (instructions). The main chat (chat1) is where the user enters their main prompt. The user can use the other text fields for instructions and background knowledge. All text fields are cleared when the user hits enter but the data is persistent.

### Login Page

The login page allows the user to log in so the chatbot recognizes who they are. the user gives their email and password, then the password is matched to a userDB entry. if an entry is not found, an invalid credentials messaged is flashed. After a successful login, the users name will be displayed whenever they send a message and thre bot will be able to access previous conversations.

### Create Account Page



### About Page

the about page contains all the on how to use the website (similar information from this document)
