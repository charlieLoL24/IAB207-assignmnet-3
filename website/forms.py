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


class CreateEvent(FlaskForm):
    """
        A form for creating events
    """
    Description = StringField("User Name", validators=[InputRequired()])
    
    Image = FileField(
        'Event Image',
        validators=[
            FileRequired(message='Please select a file name'),
            FileAllowed(ALLOWED_FILE, message='support only png, jpg, bmp')
            ]
        )

    Start_time = TimeField("Start Time", validators=[InputRequired()])
    date = DateField("Event Date", validators=[InputRequired()])
    Venue = StringField("Venue", validators=[InputRequired()])
    Category = StringField("User Name", validators=[InputRequired()])
    Tickets_avaliable = IntegerField("Tickets avaliable", validators=[InputRequired()])
    status = StringField("User Name", validators=[InputRequired()])
    
    
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
