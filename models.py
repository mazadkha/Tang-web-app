from database import db


class Note(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column("title", db.String(100))
    text = db.Column("text", db.String(400))
    status = db.Column("status", db.String(20))

    def __init__(self, title, text, status):
        self.title = title
        self.text = text
        self.status = status


class User(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column("email", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.name = email
