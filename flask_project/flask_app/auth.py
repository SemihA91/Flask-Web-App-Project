from . import db
from flask import (Blueprint, render_template, flash, redirect, url_for,
                   request, session)
from flask_app.models import User
from flask_login import login_user, login_required, logout_user
from flask_mail import Message
from . import mail

auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():

    """
    Route for the sign up page

    Parameters
    ----------
        No Parameters

    Returns
    -------
    render_template() : Function
        Renders the 'SignUp.html' page

    """
    return render_template('SignUp.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    """
    Route for the sign up function. Takes user information from the sign up
    form.
    Checks for errors in inputs and adds to database.

    Parameters
    ----------
        No Parameters

    Returns
    -------
    redirect() : Function
        Redirects to auth.signup page

    """

    # getting the information from the form
    username = request.form.get('username')
    first_name = request.form.get('first name')
    last_name = request.form.get('last name')
    email = request.form.get('email')
    password = request.form.get('password')
    conf_pass = request.form.get('confirm password')

    user_email = User.query.filter_by(email=email).first()
    user_username = User.query.filter_by(username=username).first()

    if user_email:
        flash(f'{"Email address already in use."}', "error")
        return redirect(url_for('auth.signup'))
    elif user_username:
        flash(f'{"Username already in use"}', "error")
        return redirect(url_for('auth.signup'))

    if conf_pass != password:
        flash(f'''{"Passwords don't match"}''', "error")
        return redirect(url_for('auth.signup'))

    newUser = User(username=username, first_name=first_name,
                   last_name=last_name, email=email, password=password)
    db.session.add(newUser)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():

    """
    Route for the login page

    Parameters
    ----------
        No Parameters

    Returns
    -------
    render_template() : Function
        Renders the 'login.html' page

    """

    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():

    """
    Route for the login function. Takes user information from the login form.
    Checks if the user exists and if password matches, then logs the user in.

    Parameters
    ----------
        No Parameters

    Returns
    -------
    redirect() : Function
        Redirects to auth.signup page or main.index depending on if the user
        inputs correct information.

    """

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not password == user.password:
        flash(f'{"Please check your login details and try again."}', "error")
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():

    """
    Route for the logout function. Logs the user out.

    Parameters
    ----------
        No Parameters

    Returns
    -------
    redirect() : Function
        redirects to the main.index page

    """

    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/forgot_password')
def forgot_password():

    """
    Route for the forgot password page

    Parameters
    ----------
        No Parameters

    Returns
    -------
    render_template() : Function
        Renders the 'forgot_pass.html' page

    """

    return render_template('forgot_pass.html')


@auth.route('/forgot_password', methods=['POST'])
def forgot_password_post():

    """
    Route for the forgot password function. Sends a recovery email to the
    account which forgot the password

    Parameters
    ----------
        No Parameters

    Returns
    -------
    redirect() : Function
        redirects user to the auth.login page

    """

    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("This email isn't tied to any account. Please sign up.")
        return redirect(url_for('auth.signup'))

    session['email'] = email
    msg = Message('You have asked to reset your password', recipients=[email],
                  sender='doNotReply@gmail.com')
    msg.html = """
        <div>
            <p>To reset your password, please click the following link:</p>
            <br>
            <a href='http://localhost:5000/reset'>Reset password</a>
        </div>
    """
    mail.send(msg)

    return redirect(url_for('auth.login'))


@auth.route('/reset')
def reset():
    """
    Route to reset the password

    Parameters
    ----------
        No Parameters

    Returns
    -------
    render_template() : Function
        Renders the 'reset_pass.html' page

    """
    return render_template('reset_pass.html')


@auth.route('/reset', methods=['POST'])
def reset_post():

    """
    Route for the user to set the new password. Checks if new passwords
    match and then sets it.

    Parameters
    ----------
        No Parameters

    Returns
    -------
    redirect() : Function
        redirects user to the auth.login page

    """

    password = request.form.get('password')
    conf_pass = request.form.get('confirm_password')

    if password != conf_pass:
        flash("Password don't match. Please try again")
        redirect(url_for('auth.reset'))

    user = User.query.filter_by(email=session['email']).first()
    user.password = password
    db.session.commit()
    session.pop('email', None)

    return redirect(url_for('auth.login'))
