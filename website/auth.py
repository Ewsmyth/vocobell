from flask import current_app
from flask import Blueprint, render_template, redirect, url_for, flash
from .models import User
from website.forms.auth_forms import LoginForm
from .utils import bcrypt
from flask_login import login_user, logout_user
from website import limiter

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
@limiter.limit("200 per minute")
def authLogin():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        rememberMe = form.remember.data

        userToLogin = User.query.filter_by(username=username).first()

        if not userToLogin:
            flash("Account does not exist.", "danger")
            return redirect(url_for('auth.authLogin'))

        if not userToLogin.is_active:
            flash("Account is deactivated.", "warning")
            return redirect(url_for('auth.authLogin'))

        if bcrypt.check_password_hash(userToLogin.password, password):
            login_user(userToLogin, remember=rememberMe)
            if userToLogin.first_login:
                return redirect(url_for('user.userFirstLogin', username=userToLogin.username))
            return redirect(url_for('user.userDashboard', username=userToLogin.username))
        
        flash("Incorrect password.", "danger")
        return redirect(url_for('auth.authLogin'))

    return render_template('auth-login.html', form=form)

@auth.route('/logout/', methods=['POST', 'GET'])
def authLogout():
    logout_user()
    return redirect(url_for('auth.authLogin'))
