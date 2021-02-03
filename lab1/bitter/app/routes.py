from re import error
from flask import render_template, request, redirect, session, Response
from flask.helpers import url_for

from app import app
from app.forms import LoginForm, RegisterForm, PostForm
from app.utils import (get_user_id, register_user, login_user, create_post, 
                       get_posts, get_post, create_comment, get_comments)

@app.route('/')
def index():
    username = session.get('username')
    posts = get_posts(request.args.get('filter'))
    if username:
        return render_template('index.html', username=username, posts=posts)
    return render_template('index.html', posts=posts)


@app.route('/create_post', methods=['GET', 'POST'])
def new_post():
    errors = []
    form = PostForm()
    if request.method == 'POST':
        post = create_post(form, session['username'])
        if post['status']:
            messages = ['Post created!']
            return render_template('index.html', messages=messages, username=session.get('username'))
        else:
            errors = post['errors']
    return render_template('new_post.html', form=form, username=session.get('username'), errors=errors)


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors = []
    form = LoginForm()
    if request.method == 'POST':
        login = login_user(form)
        if login['status']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            errors = login['errors']
    return render_template('login.html', title='Sign In', form=form, errors=errors)


@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = []
    form = RegisterForm()
    if request.method == 'POST':
        registration = register_user(form)
        if registration['status']:
            return redirect(url_for('login'))
        else:
            errors = registration['errors']
    return render_template('register.html', title='Register', form=form, errors=errors)


@app.route('/logout', methods=['GET'])
def logout():
    if session.get('username'):
        session.pop('username')
    return redirect(url_for('index'))

@app.route('/post/comment', methods=['POST'])
@app.route('/comment', methods=['POST'])
def comment():
    if not session.get('username'):
        return Response(status=401)

    raw_data = request.json
    data = {
        'body': raw_data['body'],
        'user_id': get_user_id(session['username']),
        'post_id': raw_data['post_id']
    }
    status = create_comment(data)

    if status['status']:
        return Response(status=200)
    return Response(status=403)


@app.route('/post/<int:id>', methods=['GET'])
def post_detail(id):
    post = get_post(id)
    if not post:
        return Response(status=404)
    comments = get_comments(id)
    return render_template('post.html', username=session.get('username'), post=post, comments=comments)
