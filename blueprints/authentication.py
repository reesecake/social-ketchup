from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user

from app.forms import RegistrationForm
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
