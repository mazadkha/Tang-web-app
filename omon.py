# FLASK Tutorial 1 -- We show the bare-bones code to get an app up and running

# imports
import os  # os is used to get environment variables IP & PORT
from flask import Flask, redirect, url_for  # Flask is the web app that we will customize
from flask import render_template, session
from flask import request
from database import db
from models import Note as Note
from models import User as User
from forms import RegisterForm
import bcrypt

app = Flask(__name__)  # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_story_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
# configure the secret key that will be used to by the app to secure session data
app.config['SECRET_KEY'] = 'SE3155'
# Setup models
with app.app_context():
    db.create_all()  # run under the app context

# stories = {
#     1: {'title': 'First note', 'text': 'This is my first note', 'status': 'Backlog'},
#     2: {'title': 'Second note', 'text': 'This is my second note', 'status': 'Backlog'},
#     3: {'title': 'Third note', 'text': 'This is my Third note', 'status': 'Backlog'}
# }
# a_user = {'name': 'Mohammad Azad', 'email': 'mogli@uncc.edu'}
company = 'TANG'


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
def index():
    a_user = db.session.query(User).filter_by(email='mazad@uncc.edu').one()
    return render_template('index.html', user=a_user, company=company)


@app.route('/dashboard')
def get_stories():
    # Retrieve user from database
    # Check if a user is saved in the session
    if session.get('user'):
        # Retrieve stories from database
        all_stories = db.session.query(Note).filter_by(user_id=session['user_id']).all()

        return render_template('dashboard.html', stories=all_stories, user=session['user'], company=company)
    else:
        return redirect(url_for('login'))


@app.route('/details/<story_id>')
def get_details(story_id):
    a_user = db.session.query(User).filter_by(email='mazad@uncc.edu').one()
    my_story = db.session.query(Note).filter_by(id=story_id).one()
    return render_template('story-detail.html', story=my_story, user=a_user, company=company)


@app.route('/dashboard/new', methods=['GET', 'POST'])
def new_story():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['noteText']
        status = request.form['status']
        story = Note(title, text, status)
        db.session.add(story)
        db.session.commit()
        return redirect(url_for('get_stories'))
    else:
        a_user = db.session.query(User).filter_by(email='mazad@uncc.edu').one()
        return render_template('new.html', user=a_user, company=company)


@app.route('/dashboard/edit/<story_id>', methods=['GET', 'POST'])
def update(story_id):
    # Check method used for request
    if request.method == 'POST':
        # Get the title data
        title = request.form['title']
        # Get the text data
        text = request.form['noteText']
        # Get the status
        status = request.form['status']
        story = db.session.query(Note).filter_by(id=story_id).one()
        # Update the data
        story.tittle = title
        story.text = text
        story.status = status

        # Update the db
        db.session.add(story)
        db.session.commit()

        # Getting back to dashboard after updating
        return redirect(url_for('get_stories'))
    else:
        # Get request - show story to be updated
        # retrieve user from db
        a_user = db.session.query(User).filter_by(email='mazad@uncc.edu').one()

        # retrieve story from db
        my_story = db.session.query(Note).filter_by(id=story_id).one()

        return render_template('new.html', story=my_story, user=a_user, company=company)


@app.route('/dashboard/delete/<story_id>', methods=['POST'])
def delete(story_id):
    # Retrieve story from database
    my_story = db.session.query(Note).filter_by(id=story_id).one()
    db.session.delete(my_story)
    db.session.commit()

    return redirect(url_for('get_stories'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Salt and hash password
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # Get entered use data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # Create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # Add user to the database
        db.session.add(new_user)
        db.session.commit()
        # Save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # accessing the id value from the newly added user
        # Show user's dashboard view
        return redirect(url_for('get_stories'))

    return render_template('register.html', form=form, company=company)


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
