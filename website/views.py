from flask import Blueprint, render_template, request, redirect, url_for
from .forms import CreateEvent, CreateUser, CreateComment, LoginForm
from .models import Event, Comment, User
from flask_login import login_required, current_user


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
            
    return render_template('details.html', event=event, comments=comment_dicts)


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main_bp.route('/history')
@login_required
def history():
    return render_template('history.html')


@main_bp.route('/user', methods=['GET', 'POST'])
def user():
    form = LoginForm()  # Create an instance of LoginForm
    if form.validate_on_submit():
        # Handle the form submission here (e.g., check credentials)
        pass
    return render_template('user.html', form=form)  # Pass the form instance
