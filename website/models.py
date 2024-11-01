from . import db
from sqlalchemy import Column, Integer, String
from datetime import datetime
from flask_login import UserMixin
import enum


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Order', backref='user')
    events = db.relationship('Event', backref=db.backref('commented_users'))

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Image = db.Column(db.String(60), nullable=False, default='default.jpg')
    Start_time = db.Column(db.Time, nullable=False)
    Start_date = db.Column(db.Date, nullable=False)
    Venue = db.Column(db.String(32), nullable=False)
    Category = db.Column(db.String(32), nullable=False)
    Tickets_available = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.String(32), nullable=False)
    
    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Order', backref='event')

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    date_posted = db.Column(db.Date, nullable=False)


    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    tickets = db.Column(db.Integer, nullable=False)
    
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))