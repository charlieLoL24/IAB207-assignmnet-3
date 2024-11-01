from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import CreateEvent, CreateComment, LoginForm, CreateOrder
from .models import Event, Comment, User, Order
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
    order_form = CreateOrder()
    user = check_login(current_user)
    
    error=""
    if(order_form.validate_on_submit()):
        tickets = order_form.tickets.data
        user = check_login(current_user)
        event = Event.query.filter_by(id=event_id).first()
        
        if tickets is None:
            error = "No tickets selected"
            
        elif not user:
            error = "You must login to purchace tickets"
            
        elif event.Tickets_avaliable <= 0:
            error = "This event is sold out"
        
        elif tickets > event.Tickets_avaliable:
            error = "There are not enough tickets avaliable to fufill your request"
            
        if error == "":
            order = Order(
                tickets = tickets,
                user_id = user.id,
                event_id = event_id
            )
            
            event.Tickets_avaliable -= tickets
            
            db.session.add(order)
            db.session.commit()
            
            return redirect(url_for('main.orderDetails') + '?id=' + str(order.id))
            
        else:
            print(error)
            flash(error)
            
    return render_template('details.html', event=event, user=user, order_form=order_form)


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@main_bp.route('/history')
@login_required
def history():
    return render_template('history.html')
    
    
@main_bp.route('/comments', methods = ['GET', 'POST'])
def Comments():
    """
        A view to display the comments form partial
    """
    comment_form = CreateComment()
    user = check_login(current_user)
    event_id = request.args.get('id')
    
    error=""
    if(comment_form.validate_on_submit()):
        comment = comment_form.comment.data
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
    print(event_id)
    comment_dicts = []
    for comment in comments:
        comment_dicts.append(
            {
                "poster": User.query.filter_by(id=comment.user_id).first().name,
                "comment": comment.comment,
                "date_posted": comment.date_posted
            }
        )
        
    return render_template('partials/comments.html', comment_form=comment_form, comments=comment_dicts, user=user)


@main_bp.route('/order', methods = ['GET'])
def orderDetails():
    order_id = request.args.get('id')
    order = Order.query.filter_by(id=order_id).first()
    event = Event.query.filter_by(id=order.event_id).first()
    user = check_login(current_user)
    
    return render_template('order.html', order=order, event=event, user=user)