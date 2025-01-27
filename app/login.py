from flask import session, flash, redirect, url_for, render_template, request
from werkzeug.security import check_password_hash
from app.form import LoginForm


class Login:

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

    @staticmethod
    def logout_user():
        """Pop out all user status in session to logout user
            """
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        session.pop('message', None)
        session.pop('admin_auth', None)








