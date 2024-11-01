from flask_wtf import FlaskForm
from wtforms.fields import (
    TextAreaField,
    SubmitField,
    StringField,
    PasswordField,
    IntegerField,
    TimeField,
    DateField,
    DateTimeField,
    SelectField,
)
from wtforms.validators import InputRequired, Length, Email, EqualTo

from flask_wtf.file import FileRequired, FileField, FileAllowed

from . import CATEGORIES

ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}

    # creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# this is the registration form


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class CreateEventForm(FlaskForm):
    event_image = FileField(
        'Event Image',
        validators=[
            FileRequired(message='Please select a file'),
            FileAllowed(ALLOWED_FILE, message='Only image files are allowed')
        ]
    )
    event_title = StringField(
        "Event Title", 
        validators=[InputRequired(), Length(max=255)]
    )
    event_description = TextAreaField(
        "Event Description", 
        validators=[InputRequired(), Length(max=500)]
    )
    event_date = DateField("Event Date", validators=[InputRequired()])
    event_time = TimeField("Event Time", validators=[InputRequired()])
    event_venue = StringField(
        "Event Venue", 
        validators=[InputRequired(), Length(max=32)]
    )
    event_genre = SelectField(
        "Event Category", 
        choices=[('', 'Select Category')] + CATEGORIES,
        validators=[InputRequired()]
    )
    tickets_available = IntegerField("Tickets Available", validators=[InputRequired()])
        
class CreateComment(FlaskForm):
    """
        A form for creating a comment
    """
    comment = StringField("Comment", validators=[InputRequired()])
    submit = SubmitField("Post")


class CreateOrder(FlaskForm):
    """
        A form for creating orders
    """
    tickets = IntegerField("Ticket Quantity", validators=[InputRequired()])
    submit = SubmitField("Post")
