from datetime import datetime
from enum import Enum

from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.validator import Validator


TABLES = {
    'post': 'public."post"',
    'user': 'public."user"',
    'comment': 'public."comment"'
}


class USER_ROLES(Enum):
    ANON = 0
    USER = 1
    MODER = 2
    ADMIN = 3


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
    data = Validator.validate_form(form)
    if not data.get('username'):
        errors.append('Username is required')
    if not data.get('email'):
        errors.append('Email is required')
    if not (data.get('password1') and data.get('password2')):
        errors.append('Password is required')
    elif data.get('password1') != data.get('password2'):
        errors.append('Passwords missmatch')
    
    if errors:
        return {'status': False, 'errors': errors}

    password = generate_password_hash(data['password1'])
    query = """INSERT INTO public."user" (username, email, passwd) VALUES """
    tail = f' (\'{data["username"]}\', \'{data["email"]}\', \'{password}\');'
    query += tail
    res = db.engine.execute(query)
    return {'status': True}


def login_user(form):
    errors = []
    data = Validator.validate_form(form)
    if not data.get('username'):
        errors.append('Username is required')
    if not  data.get('password'):
        errors.append('Password is required')
    if errors:
        return {'status': False, 'errors': errors}
    
    query = f'SELECT id, username, passwd, role FROM {TABLES["user"]} WHERE username = \'{data.get("username")}\';'
    result = db.session.execute(query).fetchall()
    if len(result) != 1:
        return {'status': False, 'errors': ['User not found']}
    user = {
        'user_id': result[0][0],
        'username': result[0][1],
        'passwd':result[0][2],
        'role': result[0][3]
    }
    if not check_password_hash(user['passwd'], data.get('password')):
         return {'status': False, 'errors': ['User not found']}
    user.pop('passwd')
    return {'status': True, 'user': user}


def create_post(form, username):
    errors = []
    data = Validator.validate_form(form)
    if not data.get('title'):
        errors.append('Title is required')
    if not data.get('body'):
        errors.append('Post can\'t be blank')
    if errors:
        return {'status': False, 'errors': errors}
    
    user_id = get_user_id(username)
    query = """INSERT INTO public."post" (title, body, pub_date, user_id) VALUES """ 
    tail = f' (\'{data["title"]}\', \'{data["body"]}\', \'{datetime.now()}\', {user_id});'
    query += tail
    db.engine.execute(query)
    return {'status': True}


def get_posts(filters=None):
    if filters:
        filters = Validator.substitute_special(filters)
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
    id = Validator.substitute_special(id)
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


def create_comment(data, user_id):
    raw_data = Validator.validate_data(data)
    data = {
        'body': raw_data['body'],
        'user_id': user_id,
        'post_id': raw_data['post_id']
    }

    if not data.get('body'):
        return {'status': False, 'errors': ['Cannot leave empty comment']}
    query = """INSERT INTO public."comment" (body, pub_date, user_id, post_id, active) VALUES """
    tail = f'(\'{data["body"]}\', \'{datetime.now()}\', \'{data["user_id"]}\', \'{data["post_id"]}\', true);'
    query += tail 
    db.engine.execute(query)
    return {'status': True}


def get_comments(post_id, limit=None):
    post_id = Validator.substitute_special(str(post_id))
    if limit:
        limit = Validator.substitute_special(str(limit))
    query = """
    SELECT u.id, u.username, c.body, c.pub_date, c.id FROM public."comment" AS c
    INNER JOIN public."post" AS p ON (c.post_id = p.id)
    INNER JOIN public."user" AS u ON (c.user_id = u.id)
    """
    tail = f'WHERE p.id = \'{post_id}\' AND c.active = true '
    limit = f' LIMIT \'{limit}\';' if limit else ';'
    order = ' ORDER BY (c.id) DESC'
    query += tail  + order + limit
    result = db.engine.execute(query).fetchall()
    return [{
        'user_id': item[0],
        'username': item[1],
        'body': Validator.validate_html(item[2]),
        'pub_date': item[3],
        'comment_id': item[4]
    } for item in result ]


def get_users_list(username):
    query = 'SELECT id, username, email, role FROM public."user" WHERE username IS DISTINCT FROM '
    tail = f"'{username}' ORDER BY (id) ASC"
    query += tail
    result = db.engine.execute(query).fetchall()
    return [{
        'user_id': item[0],
        'username': item[1],
        'email': item[2],
        'role': item[3]
    } for item in result ]


def set_user_role(data):
    data = Validator.validate_data(data)
    if data.get('user_id') and data.get('new_role'):
        query = f'UPDATE public."user" SET role = {data["new_role"]} WHERE id = {data["user_id"]};'
        db.engine.execute(query)
        return True
    return False


def delete_comment_by_id(id):
    id = Validator.substitute_special(str(id))
    try:
        valid = int(id) > 0
    except ValueError:
        valid = False

    if valid:
        query = """
        UPDATE public."comment" 
        SET active = false
        WHERE id = 
        """
        tail = f'{id};'
        query += tail
        db.engine.execute(query)
    return valid
