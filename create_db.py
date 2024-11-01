from website import db, create_app
from website.models import Event, User, Comment

import datetime

def create_db():
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    
def populate_db():
    
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    
    date = datetime.datetime(2024, 12, 25)
    time = datetime.time(12, 20)
    
    e1 = Event(
        id=1,
        Title="Test event 1",
        Status="Open",
        Category="Category 1",
        Description="A really cool event!!",
        Start_time= time,
        Start_date= date,
        Venue= 'a fun place',
        Tickets_available=10,
        Image='static.img.',
        user_id = 1
    )
    
    e2 = Event(
        id=2,
        Title="Test event 2",
        Status="Open",
        Category="Category 2",
        Description="A really cool event!!",
        Start_time= time,
        Start_date= date,
        Venue= 'a fun place',
        Tickets_available=10,
        Image='static.img.',
        user_id = 1
    )
    
    e3 = Event(
        id=3,
        Title="Test event 3",
        Status="Open",
        Category="Category 3",
        Description="A really cool event!!",
        Start_time= time,
        Start_date= date,
        Venue= 'a fun place',
        Tickets_available=10,
        Image='static.img.',
        user_id = 1
    )
    
    e4 = Event(
        id=4,
        Title="Test event 4",
        Status="Open",
        Category="Category 4",
        Description="A really cool event!!",
        Start_time= time,
        Start_date= date,
        Venue= 'a fun place',
        Tickets_available=10,
        Image='static.img.',
        user_id = 1
    )
    
    db.session.add(e1)
    db.session.add(e2)
    db.session.add(e3)
    db.session.add(e4)
    db.session.commit()
    
def add_to_db(id, Title, Status, Category, Description, Start_time, Start_date, Venue, Tickets_avaliable, Image):
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    
    event = Event(
        id = id,
        Title = Title,
        Status = Status,
        Category = Category,
        Description = Description,
        Start_time = Start_time,
        Start_date = Start_date,
        Venue = Venue,
        Tickets_avaliable = Tickets_avaliable,
        Image = Image
    )
    
    db.session.add(event)
    db.session.commit()
    
def create_user():
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    
    user = User(
        id=1,
        name = "test user",
        emailid = "test@test.com",
        password_hash = "jedftggg6747r637c2b478r"
    )
    
    db.session.add(user)
    db.session.commit()
    
def populate_comments():
    app = create_app()
    ctx = app.app_context()
    ctx.push()
    
    date = datetime.datetime(2024, 12, 25)
    time = datetime.time(12, 20)
    
    comment1 = Comment(
        id=1,
        comment = "THIS EVENT IS A CRYPTO SCAM",
        date_posted = date,
        event_id = 3,
        user_id = 1
    )
    
    comment2 = Comment(
        id=2,
        comment = "THIS EVENT IS A CRYPTO SCAM",
        date_posted = date,
        event_id = 3,
        user_id = 1
    )
    
    comment3 = Comment(
        id=3,
        comment = "pretty cool",
        date_posted = date,
        event_id = 3,
        user_id = 1
    )
    
    comment4 = Comment(
        id=4,
        comment = "awesome!!",
        date_posted = date,
        event_id = 3,
        user_id = 1
    )
    
    db.session.add(comment1)
    db.session.add(comment2)
    db.session.add(comment3)
    db.session.add(comment4)
    
    db.session.commit()
    
    
date = datetime.datetime(2024, 12, 25)
time = datetime.time(12, 20)

create_db()
    
# add_to_db(
#     id=5,
#     Title="Test event 5",
#     Status="Open",
#     Category="Category 5",
#     Description="A really cool event!!",
#     Start_time= time,
#     Start_date= date,
#     Venue= 'a fun place',
#     Tickets_avaliable=10,
#     Image='static.img.'
# )

populate_db()

create_user()

populate_comments()