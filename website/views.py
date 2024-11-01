from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import CreateEvent, CreateComment, LoginForm
from .models import Event, Comment, User
from flask_login import login_required, current_user
from datetime import datetime
from . import db


main_bp = Blueprint('main', __name__)

def check_login(current_user):

    return current_user if current_user.is_authenticated else None


@main_bp.route('/')
def index():
    user = check_login(current_user)
    events = Event.query.order_by(Event.id).all()
    return render_template('index.html', events=events, user=user)

@main_bp.route('/create-event')
@login_required
def createEvent():
    return render_template('create.html', form=CreateEvent)


@main_bp.route('/create-user')
def createUser():
    return render_template('register.html', form=CreateUser)


@main_bp.route('/details', methods = ['GET', 'POST'])
def eventDetails():
    event_id = request.args.get('id')
    event = Event.query.filter_by(id=event_id).first()
    form = CreateComment()
    user = check_login(current_user)
    
    error = ""
    if(form.validate_on_submit()):
        comment = form.comment.data
        user = check_login(current_user)
        
        if comment is None:
            error = "Please enter a comment"
            
        if not user:
            error = "You must login to post comments"
            
        if error == "":
            comment = Comment(
                comment = comment,
                date_posted = datetime.now(),
                event_id = event_id,
                user_id = user.id
            )
            
            db.session.add(comment)
            db.session.commit()
        else:
            print(error)
            flash(error)
        
    # get comment and poster then builds a list with the comment details and user
    comments = Comment.query.filter_by(event_id=event_id).all()
    comment_dicts = []
    for comment in comments:
        comment_dicts.append(
            {
                "poster": User.query.filter_by(id=comment.user_id).first().name,
                "comment": comment.comment,
                "date_posted": comment.date_posted
            }
        )
            
    return render_template('details.html', event=event, comments=comment_dicts, form=form, user=user)


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main_bp.route('/history')
@login_required
def history():
    return render_template('history.html')
