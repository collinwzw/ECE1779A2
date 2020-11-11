from app import app
from flask import render_template, redirect, url_for, request, g,session
from app.login import Login
from app.database import dbManager
from app.form import ConfigForm
from app.AutoScaller import AutoScaler

@app.route('/')
@app.route('/index')
def index():
    """Controller will assert user status, if user is already login, it will redirect to /home,
    else Controller will return the mail.html"""
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template("main.html")
    # User is not loggedin redirect to login pa ge
    else:
        return redirect(url_for('login'))


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
    if 'loggedin' in session:
        form = ConfigForm()
        AutoScaler.read_config()
        if form.validate_on_submit():
            cpu_up_threshold = form.cpu_up_threshold
            cpu_down_threshold = form.cpu_down_threshold
            cooling_time = form.cooling_time
            max_worker = form.max_worker
            min_worker = form.min_worker
            upper_ratio = form.upper_ratio
            lower_ratio = form.lower_ratio
            AutoScaler.write_config(cpu_up_threshold,cpu_down_threshold,cooling_time, max_worker,min_worker,upper_ratio,upper_ratio)
        return render_template("autoscaller.html", title="Auto Scaller", form=form, usertable= usertable)
    else:
        return redirect(url_for('login'))


@app.route('/worker/deleta_all data')
def delete_all_data():
    dbManager.dbManager.delete_all_data("accounts","error.html")
    dbManager.dbManager.delete_all_data("images","error.html")
    redirect(url_for("index"))
