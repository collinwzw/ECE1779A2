from app import app
from flask import render_template, redirect, url_for, request, g,session
from app.login import Login
from app.database import dbManager

@app.route('/')
@app.route('/index')
def index():
    """Controller will assert user status, if user is already login, it will redirect to /home,
    else Controller will return the mail.html"""
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return redirect('home')
    # User is not loggedin redirect to login pa ge
    return render_template("main.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    Login.loginadmin()


@app.route('/logout')
def logout():
    Login.logout_user()
    """Controller pop the login status and user information in session, then redirect to index page"""
    return redirect(url_for('index'))


@app.route('/worker',methods=['GET','POST'])
def worker():
    return 'block for worker details'


@app.route('/autoscaller')
def autoscaller():
    return 'block for autoscaller'


@app.route('/worker/deleta_all data')
def delete_all_data():
    dbManager.dbManager.delete_all_data("accounts","error.html")
    dbManager.dbManager.delete_all_data("images","error.html")
    redirect(url_for("index"))