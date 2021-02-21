from re import error
from flask import render_template, request, redirect, session, Response, jsonify, make_response
from flask.helpers import url_for

from app import app
from app.decorators import logging
from app.forms import LoginForm, RegisterForm, PostForm
from app.queries import (get_user_id, register_user, login_user, create_post, 
                       get_posts, get_post, create_comment, get_comments, get_users_list,
                       set_user_role, USER_ROLES, delete_comment_by_id)



@app.route('/')
@logging
def index():
    posts = get_posts(request.args.get('filter'))
    return render_template(
        'index.html', 
        posts=posts
    )


@app.route('/create_post', methods=['GET', 'POST'])
@logging
def new_post():
    errors = []
    form = PostForm()
    if request.method == 'POST':
        post = create_post(form, session['username'])
        if post['status']:
            messages = ['Post created!']
            return render_template('index.html', messages=messages)
        else:
            errors = post['errors']
    return render_template('new_post.html', form=form, errors=errors)


@app.route('/login', methods=['GET', 'POST'])
@logging
def login():
    errors = []
    form = LoginForm()
    if request.method == 'POST':
        login = login_user(form)
        if login['status']:
            session.update(login['user'])
            return redirect(url_for('index'))
        else:
            errors = login['errors']
    return render_template('login.html', title='Sign In', form=form, errors=errors)


@app.route('/register', methods=['GET', 'POST'])
@logging
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
@logging
def logout():
    if session.get('username'):
        session.pop('username')
        session.pop('role')
    return redirect(url_for('index'))

@app.route('/post/comment', methods=['POST'])
@app.route('/comment', methods=['POST'])
@logging
def comment():
    if not session.get('username'):
        return Response(status=401)

    user_id = get_user_id(session['username'])
    status = create_comment(request.json, user_id)

    if status['status']:
        return Response(status=200)
    return Response(status=403)


@app.route('/post/<int:id>', methods=['GET'])
@logging
def post_detail(id):
    post = get_post(id)
    if not post:
        return render_template('404.html')
    return render_template('post.html', post=post)


@app.route('/post/post_comments/<int:id>')
@app.route('/post_comments/<int:id>', methods=['GET'])
@logging
def get_post_comments(id):
    return jsonify(get_comments(id))


@app.route('/admin', methods=['GET'])
@logging
def admin():
    if session.get('role') != USER_ROLES.ADMIN.value:
        return render_template('404.html')
    users = get_users_list(session['username'])
    return render_template('admin.html', users=users)


@app.route('/user_list', methods=['GET'])
@logging
def user_list():
    if not session.get('role', 0) == USER_ROLES.ADMIN.value:
        return Response(status=404)
    return jsonify(get_users_list(session['username']))


@app.route('/user_role', methods=['POST'])
@logging
def user_role():
    # import pdb
    # pdb.set_trace()
    if not session.get('role', 0) == USER_ROLES.ADMIN.value:
        return Response(status=401)
    data = {
        'user_id': request.json.get('user_id'), 
        'new_role': request.json.get('new_role')
    }
    if set_user_role(data):
        return make_response(jsonify(data), 202)
    errors = {'error': 'id, new_role is required'}
    return make_response(jsonify(error), 400)


@app.route('/delete_comment/<int:id>', methods=['DELETE'])
@logging
def delete_comment(id):
    if not session.get('role', 0) in (USER_ROLES.MODER.value, USER_ROLES.ADMIN.value):
        return Response(status=401)
    if delete_comment_by_id(id):
        return Response(status=204)
    return Response(status=404)