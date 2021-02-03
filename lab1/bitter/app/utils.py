from datetime import date, datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User

TABLES = {
    'post': 'public."post"',
    'user': 'public."user"',
    'comment': 'public."comment"'
}


def get_new_id(table_name, delta=1):
    query = f'SELECT MAX(id) FROM {TABLES[table_name]};'
    res = db.session.execute(query)
    return (res.scalar() or 0) + delta


def get_user_id(username):
    query = f'SELECT id FROM {TABLES["user"]} WHERE username = \'{username}\';'
    result = db.session.execute(query).fetchall()
    return result[0][0]


def register_user(form):
    errors = []

    if not form.username.data:
        errors.append('Username is required')
    if not form.email.data:
        errors.append('Email is required')
    if not (form.password1.data and form.password2.data):
        errors.append('Password is required')
    elif form.password1.data != form.password2.data:
        errors.append('Passwords missmatch')
    
    if errors:
        return {'status': False, 'errors': errors}

    password = generate_password_hash(form.password1.data)
    query = """INSERT INTO public."user" (username, email, password) VALUES """
    tail = f' (\'{form.username.data}\', \'{form.email.data}\', \'{password}\');'
    query += tail
    res = db.engine.execute(query)
    return {'status': True}


def login_user(form):
    errors = []
    if not form.username.data:
        errors.append('Username is required')
    if not form.password.data:
        errors.append('Password is required')
    if errors:
        return {'status': False, 'errors': errors}

    query = f'SELECT username, passwd FROM {TABLES["user"]} WHERE username = \'{form.username.data}\';'
    result = db.session.execute(query).fetchall()
    if len(result) != 1:
        return {'status': False, 'errors': ['User not found']}
    user = result[0]
    if not check_password_hash(user[1], form.password.data):
         return {'status': False, 'errors': ['User not found']}

    return {'status': True}


def create_post(form, username):
    errors = []
    if not form.title.data:
        errors.append('Title is required')
    if not form.body.data:
        errors.append('Post can\'t be blank')
    if errors:
        return {'status': False, 'errors': errors}
    
    user_id = get_user_id(username)
    query = """INSERT INTO public."post" (title, body, pub_date, user_id) VALUES """ 
    tail = f' (\'{form.title.data}\', \'{form.body.data}\', \'{datetime.now()}\', {user_id});'
    query += tail
    db.engine.execute(query)
    return {'status': True}


def get_posts(filters=None):
    query = """SELECT u.username, p.title, p.body, p.pub_date, p.id FROM public."post" AS p
               INNER JOIN public."user" AS u ON (p.user_id = u.id)"""
    tail = ''
    if filters:
        tail = f" WHERE u.username LIKE \'%{filters}%\' OR p.title LIKE \'%{filters}%\'"
    order = ' ORDER BY (p.id) DESC;'
    query += tail + order
    result = db.session.execute(query).fetchall()

    posts =  [{
        'author': item[0],
        'title': item[1],
        'body': item[2],
        'posted_at': item[3].strftime("%Y-%b-%d %H:%M:%S"),
        'id': item[4]
    } for item in result ]
    for post in posts:
        post['comments'] = get_comments(post['id'], 5)
    return posts


def get_post(id):
    query = """SELECT u.username, p.title, p.body, p.pub_date, p.id FROM public."post" AS p
               INNER JOIN public."user" AS u ON (p.user_id = u.id)"""
    tail = f' WHERE p.id = \'{id}\''
    query += tail
    result = db.session.execute(query).fetchall()
    if len(result) == 1:
        item = result[0]
        return {
            'author': item[0],
            'title': item[1],
            'body': item[2],
            'posted_at': item[3].strftime("%Y-%b-%d %H:%M:%S"),
            'id': item[4]
        }
    else:
        return None


def create_comment(data):
    if not data.get('body'):
        return {'status': False, 'errors': ['Cannot leave empty comment']}
    query = """INSERT INTO public."comment" (body, pub_date, user_id, post_id) VALUES """
    tail = f'(\'{data["body"]}\', \'{datetime.now()}\', \'{data["user_id"]}\', \'{data["post_id"]}\');'
    query += tail 
    db.engine.execute(query)
    return {'status': True}


def get_comments(post_id, limit=None):
    query = """
    SELECT u.id, u.username, c.body, c.pub_date, c.id FROM public."comment" AS c
    INNER JOIN public."post" AS p ON (c.post_id = p.id)
    INNER JOIN public."user" AS u ON (c.user_id = u.id)
    """
    tail = f'WHERE p.id = \'{post_id}\''
    limit = f' LIMIT \'{limit}\';' if limit else ';'
    order = ' ORDER BY (c.id) DESC'
    query += tail  + order + limit
    result = db.engine.execute(query).fetchall()
    return [{
        'user_id': item[0],
        'username': item[1],
        'body': item[2],
        'pub_date': item[3],
        'comment_id': item[4]
    } for item in result ]
