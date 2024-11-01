from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import CreateEvent, CreateComment, LoginForm, CreateOrder, CreateUser  # Ensure all forms are imported
from .models import Event, Comment, User, Order
from flask_login import login_required, current_user
from datetime import datetime
from . import db

main_bp = Blueprint('main', __name__)

# Helper function to check if user is authenticated
def check_login(current_user):
    return current_user if current_user.is_authenticated else None

# Index route, displays all events
@main_bp.route('/')
def index():
    user = check_login(current_user)
    events = Event.query.order_by(Event.id).all()
    return render_template('index.html', events=events, user=user)

# Route to create a new event (only accessible when logged in)
@main_bp.route('/create-event')
@login_required
def createEvent():
    return render_template('create.html', form=CreateEvent)

# Route to create a new user account (registration page)
@main_bp.route('/create-user')
def createUser():
    return render_template('register.html', form=CreateUser)

# Event details page, shows event information and allows order and comment submission
@main_bp.route('/details', methods=['GET', 'POST'])
def eventDetails():
    event_id = request.args.get('id')
    event = Event.query.filter_by(id=event_id).first()
    order_form = CreateOrder()
    comment_form = CreateComment()
    user = check_login(current_user)
    
    error = ""
    
    # Handling ticket orders
    if order_form.validate_on_submit() and 'tickets' in request.form:
        tickets = order_form.tickets.data

        if tickets is None:
            error = "No tickets selected"
        elif not user:
            error = "You must login to purchase tickets"
        elif event.Tickets_avaliable <= 0:
            error = "This event is sold out"
        elif tickets > event.Tickets_avaliable:
            error = "Not enough tickets available to fulfill your request"

        if error == "":
            order = Order(
                tickets=tickets,
                user_id=user.id,
                event_id=event_id
            )
            event.Tickets_avaliable -= tickets
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('main.orderDetails') + '?id=' + str(order.id))
        else:
            flash(error)

    # Handling comments
    if comment_form.validate_on_submit() and 'comment' in request.form:
        comment_text = comment_form.comment.data

        if comment_text is None:
            error = "Please enter a comment"
        elif not user:
            error = "You must login to post comments"

        if error == "":
            comment = Comment(
                comment=comment_text,
                date_posted=datetime.now(),
                event_id=event_id,
                user_id=user.id
            )
            db.session.add(comment)
            db.session.commit()
        else:
            flash(error)

    # Get comments and poster details
    comments = Comment.query.filter_by(event_id=event_id).all()
    comment_dicts = [
        {
            "poster": User.query.filter_by(id=comment.user_id).first().name,
            "comment": comment.comment,
            "date_posted": comment.date_posted
        }
        for comment in comments
    ]

    return render_template('details.html', event=event, user=user, order_form=order_form, comment_form=comment_form, comments=comment_dicts)

# Profile page, accessible only when logged in, and passes user data to the template
@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# History page - shows the user's past orders
@main_bp.route('/history')
@login_required
def history():
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', user_orders=user_orders)

# Comment partial view route
@main_bp.route('/comments', methods=['GET', 'POST'])
def Comments():
    comment_form = CreateComment()
    user = check_login(current_user)
    event_id = request.args.get('id')
    
    error = ""
    if comment_form.validate_on_submit():
        comment_text = comment_form.comment.data

        if comment_text is None:
            error = "Please enter a comment"
        elif not user:
            error = "You must login to post comments"

        if error == "":
            new_comment = Comment(
                comment=comment_text,
                date_posted=datetime.now(),
                event_id=event_id,
                user_id=user.id
            )
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash(error)
            
    comments = Comment.query.filter_by(event_id=event_id).all()
    comment_dicts = [
        {
            "poster": User.query.filter_by(id=comment.user_id).first().name,
            "comment": comment.comment,
            "date_posted": comment.date_posted
        }
        for comment in comments
    ]
    
    return render_template('partials/comments.html', comment_form=comment_form, comments=comment_dicts, user=user)

# Order details route
@main_bp.route('/order', methods=['GET'])
def orderDetails():
    order_id = request.args.get('id')
    order = Order.query.filter_by(id=order_id).first()
    event = Event.query.filter_by(id=order.event_id).first()
    user = check_login(current_user)
    
    return render_template('order.html', order=order, event=event, user=user)
