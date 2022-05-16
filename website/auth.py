from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
#This will allow us to use a hash for a password for security, so we not store it in a plaintext
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
#Current user function can be used as we already use a UserMixin
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

#Defining root with an appropriate method requests
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #We look in the database entries for a specific user with a specific email
        user = User.query.filter_by(email=email).first()
        if user:
            #Checking for validity of a hashed password if the same
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                #Remembering user until server restarts or browser cookies clean-up
                login_user(user, remember=True)
                #If login successfull, user is redirected to the home page
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
#This decorator will make sure we can logout only after login first
@login_required
def logout():
    logout_user()
    #After logout user is redirected to the login page
    return redirect(url_for('auth.login'))

#Defining a root with an appropriate method requests
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #We look in the database entries for a specific user with a specific email
        user = User.query.filter_by(email=email).first()
        if user:
            #Alerting user about an error by using a flash function imported above to flash a message on the screen
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:

            #We create a new user with all the details
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            #We now add this user to our database
            db.session.add(new_user)
            #We commit the changes
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            #Redirection for another page (home in this instance), by the use of a redirect funcion imported above
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
