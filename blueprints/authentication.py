from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, logout_user, login_user

from app.forms import RegistrationForm, LoginForm
from models import User

authenticationController = Blueprint("authentication", __name__)


@authenticationController.route("/signup", methods=['GET', 'POST'])
def signup():
    """
    Presents an anonymous user with the registration form and adds their info to the database.
    Uses user.set_password() to hash their password (instead of storing it plaintext).
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # hashes the given password
        user.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))

    return render_template('registration.html', form=form)


@authenticationController.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gives an anonymous user the login form and checks their credentials against users in the database.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@authenticationController.route('/logout')
def logout():
    """
    Logs the current_user out and redirects them to index.
    """
    logout_user()
    return redirect(url_for('index'))
