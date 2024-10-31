from flask import Blueprint, render_template
from .forms import CreateEvent, CreateUser, CreateComment
from .models import Event

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


@main_bp.route('/event-details')
def eventDetails():
    return render_template('details.html')


@main_bp.route('/profile')
def profile():
    return render_template('profile.html')

@main_bp.route('/history')
def history():
    return render_template('history.html')


@main_bp.route('/user')
def user():
    return render_template('user.html')
