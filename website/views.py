from flask import Blueprint, render_template, request
from .forms import CreateEvent, CreateUser, CreateComment
from .models import Event, Comment, User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    events = Event.query.order_by(Event.id).all()
    return render_template('index.html', events=events)


@main_bp.route('/create-event')
def createEvent():
    return render_template('create.html', form=CreateEvent)


@main_bp.route('/create-user')
def createUser():
    return render_template('register.html', form=CreateUser)


@main_bp.route('/details')
def eventDetails():
    event_id = request.args.get('id')
    event = Event.query.filter_by(id=event_id).first()
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
        
    print(comment_dicts)
        
    return render_template('details.html', event=event, comments=comment_dicts)


@main_bp.route('/profile')
def profile():
    return render_template('profile.html')


@main_bp.route('/history')
def history():
    return render_template('history.html')


@main_bp.route('/user')
def user():
    return render_template('user.html')
