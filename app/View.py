from app import app
from flask import render_template, redirect, url_for, request, g


@app.route('/')
@app.route('/index')
def index():
    """Controller will assert user status, if user is already login, it will redirect to /home,
    else Controller will return the mail.html"""

        # User is loggedin show them the home page

    # User is not loggedin redirect to login pa ge
    return render_template("main.html",title="Landing Page")