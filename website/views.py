from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .forms import CreateComment, LoginForm, CreateOrder, CreateEventForm
from .models import Event, Comment, User, Order
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from . import db, CATEGORIES
import os


main_bp = Blueprint('main', __name__)

# Helper function to check if user is authenticated
def check_login(current_user):
    return current_user if current_user.is_authenticated else None

# Index route, displays all events
@main_bp.route('/')
def index():
    category = request.args.get("category")
    search_keywords = request.args.get("search_keywords")
    if category or search_keywords:
        if category != "None" and search_keywords != "None":
            events = Event.query.filter(Event.Title.contains(search_keywords)).filter_by(Category=category).order_by(Event.id).all()
        elif category != "None":
            events = Event.query.filter_by(Category=category).order_by(Event.id).all()
        elif search_keywords != "None":
            events = Event.query.filter(Event.Title.contains(search_keywords)).order_by(Event.id).all()
        else:
            events = Event.query.order_by(Event.id).all()
    else:
            events = Event.query.order_by(Event.id).all()
    
    user = check_login(current_user)
    
    for event in events:
        if event.Start_date.strftime('%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d') and event.Status != "Inactive":
            new_event = Event.query.filter_by(id=event.id).first()
            new_event.Status = "Inactive"
            db.session.add(new_event)
            
    db.session.commit()        
    
    return render_template('index.html', events=events, user=user, categories=CATEGORIES, category=category, search_keywords=search_keywords)


@main_bp.route('/create-event', methods=['GET', 'POST'])
def CreateEvent():
    form = CreateEventForm()
    if form.validate_on_submit():
        # Process form data
        title = form.event_title.data
        description = form.event_description.data
        start_date = form.event_date.data
        start_time = form.event_time.data
        venue = form.event_venue.data
        category = form.event_genre.data
        tickets_available = form.tickets_available.data

        # Handle image upload
        image_file = form.event_image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
        else:
            image_path = 'default.jpg'  # Path to a default image if needed

        # Create an Event object
        new_event = Event(
            Title=title,
            Description=description,
            Image=image_path,
            Start_date=start_date,
            Start_time=start_time,
            Venue=venue,
            Category=category,
            Tickets_available=tickets_available,
            Status="Open",
            user_id=current_user.id  # assuming logged-in user
        )

        # Add and commit the new event to the database
        db.session.add(new_event)
        db.session.commit()
        
        flash("Event created successfully!", "success")
        return redirect(url_for('main.index'))

    # If validation fails, flash errors
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "error")

    return render_template('create.html', form=form)


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
    event_creator = User.query.filter_by(id=event.user_id).first()
    
    img_location = "/".join(event.Image.split("\\")[2:4])

    if event == None:
        return redirect(url_for('main.notFound'))
        
        
    error = ""
    # Handling ticket orders
    if order_form.validate_on_submit() and 'tickets' in request.form:
        tickets = order_form.tickets.data
        event_id = request.args.get('id')
        event = Event.query.filter_by(id=event_id).first()

        if event.Status == "Inactive":
            error = "This event is inactive"
        elif event.Status == "Cancelled":
            error = "This event has expired"
        elif tickets is None:
            error = "No tickets selected"
        elif not user:
            error = "You must login to purchase tickets"
        elif event.Tickets_available <= 0:
            error = "This event is sold out"
        elif tickets > event.Tickets_available:
            error = "Not enough tickets available to fulfill your request"

        if error == "":
            order = Order(
                tickets=tickets,
                user_id=user.id,
                event_id=event_id
            )
            event.Tickets_available -= tickets
            if event.Tickets_available <= 0:
                event.Status = "Sold Out"
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('main.orderDetails') + '?id=' + str(order.id))
        else:
            flash(error)

    # Get comments and poster details
    comments = Comment.query.filter_by(event_id=event_id).all()
    comment_dicts = [
        {
            "poster": User.query.filter_by(id=comment.user_id).first().name,
            "comment": comment.comment,
            "date_posted": comment.date_posted,
        }
        for comment in comments
    ]
    return render_template('details.html', event=event, user=user, order_form=order_form, comment_form=comment_form, comments=comment_dicts, event_creator=event_creator, status=event.Status, img_location=img_location)

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
    orders = []
    for order in user_orders:
        orders.append({
            "order": order,
            "event": Event.query.filter_by(id=order.event_id).first()
            })
    return render_template('history.html', orders=orders)

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


@main_bp.route('/404')
def notFound():
    return render_template("404.html")
