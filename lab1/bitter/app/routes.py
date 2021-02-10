from flask import render_template, request, redirect, session, Response, jsonify
from flask.helpers import url_for

from app import app
from app.forms import LoginForm, RegisterForm, PostForm
from app.utils import (get_user_id, register_user, login_user, create_post, 
                       get_posts, get_post, create_comment, get_comments)


ADMIN = 'admin'


@app.route('/')
def index():

    posts = get_posts(request.args.get('filter'))
    return render_template(
        'index.html', 
        username=session.get('username'), 
        user_is_admin=session.get('user_is_admin'),
        posts=posts
    )


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
            session['username'] = login['user'][0]
            session['user_is_admin'] = session['username'] == ADMIN
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
        session['user_is_admin'] = None
    return redirect(url_for('index'))

@app.route('/post/comment', methods=['POST'])
@app.route('/comment', methods=['POST'])
def comment():
    if not session.get('username'):
        return Response(status=401)

    user_id = get_user_id(session['username'])
    status = create_comment(request.json, user_id)

    if status['status']:
        return Response(status=200)
    return Response(status=403)


@app.route('/post/<int:id>', methods=['GET'])
def post_detail(id):
    post = get_post(id)
    if not post:
        return Response(status=404)
    comments = get_comments(id)
    # return render_template('post.html', username=session.get('username'), post=post, comments=comments)
    return render_template('post.html', username=session.get('username'), post=post)


@app.route('/post/post_comments/<int:id>')
@app.route('/post_comments/<int:id>', methods=['GET'])
def get_post_comments(id):
    return jsonify(get_comments(id))


@app.route('/admin', methods=['GET'])
def admin():
    return render_template(
        'admin.html',
        username=session.get('username'),
        user_is_admin=session.get('user_is_admin'),
    )