from website import db, create_app
from website.models import Event

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
    db.create_all()
    
    date = datetime.datetime(2024, 12, 25)
    time = datetime.time(12, 20)
    
    e1 = Event(
        id=1,
        Title="Test event 1",
        Status="Active",
        Category="Category 1",
        Description="A really cool event!!",
        Start_time= time,
        Start_date= date,
        Venue= 'a fun place',
        Tickets_avaliable=10,
        Image='static.img.'
    )
    
    e2 = Event(
        id=2,
        Title="Test event 2",
        Status="Active",
        Category="Category 2",
        Description="A really cool event!!",
        Start_time= time,
        Start_date= date,
        Venue= 'a fun place',
        Tickets_avaliable=10,
        Image='static.img.'
    )
    
    e3 = Event(
        id=3,
        Title="Test event 3",
        Status="Active",
        Category="Category 3",
        Description="A really cool event!!",
        Start_time= time,
        Start_date= date,
        Venue= 'a fun place',
        Tickets_avaliable=10,
        Image='static.img.'
    )
    
    e4 = Event(
        id=4,
        Title="Test event 4",
        Status="Active",
        Category="Category 4",
        Description="A really cool event!!",
        Start_time= time,
        Start_date= date,
        Venue= 'a fun place',
        Tickets_avaliable=10,
        Image='static.img.'
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
    
date = datetime.datetime(2024, 12, 25)
time = datetime.time(12, 20)
    
add_to_db(
    id=5,
    Title="Test event 5",
    Status="Open",
    Category="Category 5",
    Description="A really cool event!!",
    Start_time= time,
    Start_date= date,
    Venue= 'a fun place',
    Tickets_avaliable=10,
    Image='static.img.'
)