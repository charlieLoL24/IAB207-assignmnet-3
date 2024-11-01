from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        uname = register_form.username.data
        email = register_form.email.data
        pwd = register_form.password.data
        # utype = register_form.usertype.data
        # Check if username or email already exists
        existing_user = User.query.filter_by(name=uname).first()
        if existing_user:
            flash("Username already taken", "error")
            return render_template('register.html', form=register_form, heading='Register')

        # Hash the password for security
        pwd_hash = generate_password_hash(pwd)
        
        # Create a new User object and add it to the session
        new_user = User(name=uname, emailid=email, password_hash=pwd_hash)
        db.session.add(new_user)
        db.session.commit()
        print("added data to database") 
        flash("Registered user successfully", "success")
        
        login_user(new_user )
        return redirect(url_for('main.index'))
    else:
        print(register_form.errors)  # Display any validation errors

    # Flash validation errors, if any
    for field, errors in register_form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", "error")
    
    return render_template('register.html', form=register_form, heading='Register', user=None)



@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    error=None
    if(form.validate_on_submit()):
        user_name = form.user_name.data
        password = form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        
        #if there is no user with that name
        if u1 is None:
            error='Incorrect user name'
        #check the password - notice password hash function
        elif not check_password_hash(u1.password_hash, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
        #all good, set the login_user
            login_user(u1)
            return redirect(url_for('main.index'))
        else:
            print(error)
            flash(error)
        #it comes here when it is a get method
    return render_template('user.html', form=form, heading='Login', user=None)


@auth_bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.index'))



