from flask import session, flash, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired,Email, EqualTo, length
from werkzeug.security import generate_password_hash,check_password_hash


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(max=25,min=5,message='Username length should between 5~25')])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    password1 = PasswordField('Password', validators=[DataRequired(message='Not Allowed Empty Password'),Length(min=5,message='Password length should greater than 5')])
    password2 = PasswordField('Please Repeat Password', validators=[DataRequired(), EqualTo('password1')])
    admin_auth = BooleanField('Admin')
    submit = SubmitField('Add a new User')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Empty Username')])
    password = PasswordField('Password', validators=[DataRequired(message='Empty Password')])
    submit = SubmitField('Login')

class login:

    @staticmethod
    def loginadmin():
        form = LoginForm()
        if request.method == "GET":
            return render_template('login.html', title='Sign In', form=form)
        if request.method == "POST":
            if 'loggedin' in session:
                return redirect(url_for('home'))
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                admin_password_hash = "pbkdf2:sha256:150000$tvvCWm0V$00613fab0c6f8459297926b0005e0cf83dad8a8d858b6edf184125346f595207"
                if username == "manager":
                    if check_password_hash(admin_password_hash, password):
                        session['loggedin'] = True
                        flash('Login successfully!')
                        return redirect(url_for('index'))
                    else:
                        flash('Invalid username or password')
                        return redirect(url_for('login'))
                flash('Invalid username or password')
                return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))




@app.route('/admin/adduser', methods=['GET', 'POST'])
def add_new_user():
    if session.get('admin_auth'):
        form = AddUserForm()
        if form.validate_on_submit():
            username = form.username.data
            password_hash = generate_password_hash(form.password1.data)
            email = form.email.data
            admin_auth = form.admin_auth.data
            db = get_db()
            cursor = db.cursor(dictionary=True)
            query = "SELECT * FROM accounts WHERE username = %s or email = %s"
            cursor.execute(query, (username, email))
            account = cursor.fetchone()
            if account:
                flash('This User name or Email is existing')
                return redirect(url_for('add_new_user'))
            else:
                db = get_db()
                cursor = db.cursor(dictionary=True)
                cursor.execute("Insert into accounts (username, password_hash, email,admin_auth) "
                               "values (%s, %s, %s, %s)", (username, password_hash, email,admin_auth))
                cursor.execute("commit")
                flash("You have add a new user successfully")
                return redirect(url_for('add_new_user'))



