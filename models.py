from database import db
import datetime
# the file that creates the database


class Note(db.Model):
    # specific id of the note stored in database
    # Data table is built up of data columnns. Each column is entry for the name of the column.
    # The name of the first column is id. 
    # primary key is the specific key of the note
    id = db.Column("id", db.Integer, primary_key=True)
    # The title of the note being stored
    title = db.Column("title", db.String(200))
    # The text of the note
    text = db.Column("text", db.String(1000))
    # The status of the note
    status = db.Column("status", db.String(20))
    # Can create a foreign key; Referencing the id variable in the user class, so that 
    # nullable false means the field cannot be blanks
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # note has relationship with many comments.
    comments = db.relationship("Comment", backref="note", cascade="all, delete-orphan", lazy=True)
    # note has relationship with images uploaded.
    #image = db.relationship("Image", backref="note", cascade="all, delete-orphan", lazy=True)
    # note has relationship with many images. 
    #Initializer will create the note object. Once we use initializer object, its committed to the database.
    def __init__(self, title, text, status, user_id):
        self.title = title
        self.text = text
        self.status = status
        self.user_id = user_id

class User(db.Model):
    # primary key is the specific key of the user
    id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column("first_name", db.String(100))
    last_name = db.Column("last_name", db.String(100))
    email = db.Column("email", db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    notes = db.relationship("Note", backref="user", lazy=True)
    comments = db.relationship("Comment", backref="user", lazy=True)
    #image = db.relationship("Image", backref="user", cascade="all, delete-orphan", lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()


class Comment(db.Model):
    # the id is the primary key for the commment
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    # foreign key is referencing or associating the note the id of the note that the comment is falling under.
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=False)
    # user id is referencing the assocation of the user in the database.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, content, note_id, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.note_id = note_id
        self.user_id = user_id

""" class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.BLOB, nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, image, note_id, user_id):
        self.date_posted = datetime.date.today()
        self.image = image
        self.note_id = note_id
        self.user_id = user_id """


        
