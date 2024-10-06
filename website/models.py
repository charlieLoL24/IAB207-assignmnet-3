import enum
from . import db
from datetime import datetime
from flask_login import UserMixin


class StatusEnum(enum.Enum):
    open = "Open"
    inactive = "Inactive"
    sold_out = "Sold Out"
    cancelled = "Cancelled"


class CategoryEnum(enum.Enum):
    music = "Music"
    cosplay = "Cosplay"
    show = "Show"
    learning = "Learning"


class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    Password_hash = db.Column(db.String(64), nullable=False)
    mobile_number = db.Column(db.String(64), nullable=False)


class Event(db.Model):
    __tablename__ = 'Event'
    id = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Enum(StatusEnum), nullable=False, default=StatusEnum.open)
    Description = db.Column(db.Text, nullable=False)
    Image = db.Column(db.Text, nullable=False)
    Start_time = db.Column(db.Datetime, default=datetime.utcnow)
    Date = db.Column(db.DateTime, default=datetime.utcnow)
    Venue = db.Column(db.String(256), nullable=False)
    Category = db.Column(db.Enum(CategoryEnum), nullable=False)
    Tickets_available = db.Column(db.Integer, nullable=False)

    Creator = db.relationship("User", backref="Event")
    Comments = db.relationship("Comment", backref="Event")


class Comment(db.Model):
    __tablename__ = "Comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow())

    Creator = db.relationship("User", backref="Comment")


class Order(db.Model):
    __tablename__ = "Order"
    id = db.Column(db.Integer, primary_key=True)


