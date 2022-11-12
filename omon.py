# FLASK Tutorial 1 -- We show the bare-bones code to get an app up and running

# imports
import os  # os is used to get environment variables IP & PORT
from flask import Flask, redirect, url_for  # Flask is the web app that we will customize
from flask import render_template
from flask import request

app = Flask(__name__)  # create an app
stories = {
    1: {'title': 'First note', 'text': 'This is my first note', 'status': 'Backlog'},
    2: {'title': 'Second note', 'text': 'This is my second note', 'status': 'Backlog'},
    3: {'title': 'Third note', 'text': 'This is my Third note', 'status': 'Backlog'}
}
a_user = {'name': 'Mohammad Azad', 'email': 'mogli@uncc.edu'}
company = 'TANG'


# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
def index():
    return render_template('index.html', user=a_user, company=company)


@app.route('/dashboard')
def get_stories():
    return render_template('dashboard.html', stories=stories, user=a_user, company=company)


@app.route('/details/<story_id>')
def get_details(story_id):
    return render_template('story-detail.html', story=stories[int(story_id)], user=a_user, company=company)


@app.route('/new', methods=['GET', 'POST'])
def new_story():
    print('request method: ', request.method)
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['noteText']
        status = request.form['status']
        ids = len(stories) + 1
        stories[ids] = {'title': title, 'text': text, 'status': status}
        return redirect(url_for('get_stories'))
    else:
        return render_template('new.html', user=a_user, company=company)


app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production.
