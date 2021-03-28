from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user

from api import app
from app.forms import LoginForm, RegistrationForm
from models import User


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        user = User(username=registration_form.username.data, email=registration_form.email.data)
        user.set_password(registration_form.password.data)  # hashes the given password
        user.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('authentication.login'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.objects(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=login_form.remember_me.data)
        return redirect(url_for('home'))

    return render_template('index.html', LoginForm=login_form, RegistrationForm=registration_form)


@app.route('/home')
def home():
    return render_template('home.html')
