from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    error=None
    if(form.validate_on_submit()):
        user_name = form.user_name.data
        password = form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        print(user_name, password)
            #if there is no user with that name
        if u1 is None:
            error='Incorrect user name'
        #check the password - notice password hash function
        # elif not check_password_hash(u1.password_hash, password): # takes the hash and password
        elif not u1.password_hash == password:
            error='Incorrect password'
        if error is None:
        #all good, set the login_user
            login_user(u1)
            return redirect(url_for('main.index'))
        else:
            print(error)
            flash(error)
        #it comes here when it is a get method
    return render_template('user.html', form=form, heading='Login')


@auth_bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.index'))

@auth_bp.route('/register')
def register():
  return "wip"