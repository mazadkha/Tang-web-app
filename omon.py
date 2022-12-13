# FLASK Tutorial 1 -- We show the bare-bones code to get an app up and running

# imports
import os  # os is used to get environment variables IP & PORT
from flask import Flask, redirect, url_for  # Flask is the web app that we will customize
from flask import render_template, session
from flask import request
from database import db 
from werkzeug.utils import secure_filename
from models import Note as Note, Comment as Comment
from models import User as User
from forms import RegisterForm, LoginForm, CommentForm, ImageForm
import bcrypt

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)  # create an app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_story_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'
#  Bind SQLAlchemy db object to this Flask app



db.init_app(app)
# configure the secret key that will be used to by the app to secure session data
# key that it needs to unlock and access the data it gets there.

#UPLOAD_FOLDER = '/Users/sashankpyndi/ITSC3155/'
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
    # Check if a user is saved in the session
    # Checks if the user is logged in
    # Session has the currently logged in user information.
    if session.get('user'):
      return render_template('index.html', user=session['user'], company=company)
    return render_template('index.html', company=company)


@app.route('/dashboard')
def get_stories():
    # Retrieve user from database
    # Check if a user is saved in the session
    if session.get('user'):
        # Retrieve stories from database
        # all entries of the query
        all_stories = db.session.query(Note).filter_by(user_id=session['user_id']).all()

        return render_template('dashboard.html', stories=all_stories, user=session['user'], company=company)
    else:
        return redirect(url_for('login'), company=company)


@app.route('/details/<story_id>')
def get_details(story_id):
    # Check if a user is saved in the session
    if session.get('user'):
        # Retrieve story from database as per the story id
        # only be one entry for the query
        my_story = db.session.query(Note).filter_by(id=story_id).one()
        form = CommentForm()
        # Create a comment form object
        return render_template('story-detail.html', story=my_story, user=session['user'], company=company, form=form)
    else:
        return redirect(url_for('login'), company=company)


@app.route('/dashboard/new', methods=['GET', 'POST'])
def new_story():
    # Check if a user is saved in the session
    if session.get('user'):
        # Check method for request
        if request.method == 'POST':
            #  Get title data
            # gets the title from the form object.
            title = request.form['title']
            # gets the text from the form
           
            text = request.form['noteText']
            # gets the status form
            status = request.form['status']
             
            # associatated with the session is the currently login user. The name and id form user datatable.
            # creates note based on the user input of the form
            story = Note(title, text, status, session['user_id'])
            db.session.add(story)
            db.session.commit() 
            return redirect(url_for('get_stories'))
        else:
            # Get request - Show new note form
            return render_template('new.html', user=session['user'], company=company)
    else:
        # User is not in the session, redirect to log in
        return redirect(url_for('login'))


@app.route('/dashboard/edit/<story_id>', methods=['GET', 'POST'])
def update(story_id):
    # Check if a user is saved in the session
    if session.get('user'):
        # Check method used for request
        if request.method == 'POST':
            # Get the title data
            title = request.form['title']
            # Get the text data
            text = request.form['noteText']
            # Get the status
            status = request.form['status']
            # get the thing with story id passed in. One story with this id. Only one entry with this particular story id.
            story = db.session.query(Note).filter_by(id=story_id).one()
            # Update the data of each to the new note
            story.title = title
            story.text = text
            story.status = status

            # Update the db
            db.session.add(story)
            db.session.commit()

            # Getting back to dashboard after updating
            return redirect(url_for('get_stories'))
        else:
            # Get request - show story to be updated

            # retrieve story from db
            my_story = db.session.query(Note).filter_by(id=story_id).one()

            return render_template('new.html', story=my_story, user=session['user'], company=company)
    else:
        # User is not in the session, redirect to login
        return redirect(url_for('login'))


@app.route('/dashboard/delete/<story_id>', methods=['POST'])
def delete(story_id):
    # Check if a user is saved in the session
    if session.get('user'):
        # Retrieve story from database
        my_story = db.session.query(Note).filter_by(id=story_id).one()
        db.session.delete(my_story)
        db.session.commit()

        return redirect(url_for('get_stories'))
    else:
        # User is not in the session, redirect to login
        return redirect(url_for('login'))


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


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_stories'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form, company=company)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form, company=company)


@app.route('/logout')
def logout():
    # check if a user is saved in session
    if session.get('user'):
        session.clear()

    return redirect(url_for('index'))


@app.route('/dashboard/<story_id>/comment', methods=['POST'])
def new_comment(story_id):
    if session.get('user'):
        comment_form = CommentForm()
        # validate_on_submit only validates using POST
        if comment_form.validate_on_submit():
            # get comment data
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(story_id), session['user_id']) 
            db.session.add(new_record)
            db.session.commit()

        return redirect(url_for('get_details', story_id=story_id))
    else:
        return redirect(url_for('login'))

 #def allowed_file(filename):
    #return '.' in filename and 
     # filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
      #@app.route('/dashboard/<story_id>/image', methods=['POST'])
#def upload_image(story_id):
      
    #if session.get('user'):
     #validate_on_submit only validates using POST
       #image_form = ImageForm()
        #if image_form.validate_on_submit():
          #image = request.files['image']
           
       #return redirect(url_for('get_details',story_id=story_id)) 
    #else:
        #return redirect(url_for('login')) 

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
