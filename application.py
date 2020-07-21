import os
import cryptography
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, redirect, render_template, url_for , session, request, flash, redirect
from datetime import timedelta
import psycopg2
import requests
import json
from flask import jsonify
from cryptography.fernet import Fernet

key = Fernet.generate_key()

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home")
def index():
    question_list = db.execute("SELECT question FROM questions").fetchall()
    return render_template("index.html", question_list=question_list)

@app.route('/signup')

def signInLink():
    return render_template('signup.html')

@app.route('/ask')
def ask():
    question_list = db.execute("SELECT question FROM questions").fetchall()
    email = ""
    success = ""
    return render_template('login.html', question_list = question_list, email=email, success=success)




@app.route('/home', methods = [ "POST"])
def login():
    
    if request.method == "GET":
        return("Cannot access directly")
    
    
    global username 
    username= request.form.get("username")
    password = request.form.get("password")
    user_id = db.execute("SELECT id FROM users WHERE username = :username AND password = :password", {"username":username, "password":password}).fetchall()
    
    user_check = db.execute("SELECT * FROM users WHERE username = :username AND password = :password", {"username":username, "password":password}).fetchall()
    if user_check:
        username = username
        question_list = db.execute("SELECT question FROM questions").fetchall()
        email = ""
        success = ""
        return render_template("login.html", username = username, question_list=question_list, email=email, success=success)

        
    warn = "Wrong Username Or Password"
    return render_template("index.html", warn = warn)
    

@app.route('/ask',methods = ["POST"])
def postQ():
    question_list = db.execute("SELECT question FROM questions").fetchall()
    
    
    question = request.form.get("question")
    
    email = db.execute("SELECT email FROM users WHERE username = :username", {"username":username}).fetchone()
    db.execute("INSERT INTO questions (question, username) VALUES (:question, :username)", {"question":question, "username":username})
    db.execute("COMMIT")
    
    question_list = db.execute("SELECT question FROM questions").fetchall()
    id_list = db.execute("SELECT id FROM questions").fetchall()
    
    success2 = "Our team will come back as soon as possible! We'll email you at "
    success = "Upload Successful!"
    
    return render_template("login.html", question_list = question_list, success=success, id_list = id_list, email = email, success2=success2, username=username)
    
    
#actual signup logic
@app.route('/signup', methods = ["GET", "POST"])

def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    repassword = request.form.get("repass")
    email = request.form.get("email")
    
    #Check if username & password are not empty
    
    if email == "":
        warn = "Please enter email"
        return render_template("signup.html", warn = warn)
    if repassword == "":
        warn = "Please re-enter the password"
        return render_template("signup.html", warn = warn)
    if repassword != password:
        warn = "Passwords do not match"
        return render_template("signup.html", warn = warn)
    if username == "":
        warn = "Please enter username or password"
        return render_template("signup.html", warn = warn)
    if password == "":
        warn = "Please enter username or password"
        return render_template("signup.html", warn = warn)
    #Check username Exists
    
    user_object = db.execute("SELECT * FROM users WHERE username = :username",{"username":username}).fetchall()
    if user_object:
        warn = "Someone else has taken this username"
        return render_template("signup.html", warn = warn)
    
    # Add user to DB
    user = db.execute("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)", {"username":username, "password":password, "email":email})
    db.execute("COMMIT")
    success = "Account Created Successfully"
    return render_template("signup.html", success = success)

    
@app.errorhandler(404)
def error404(error):
    return render_template("error.html")