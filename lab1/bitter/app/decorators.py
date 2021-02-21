from datetime import datetime
from functools import wraps

from flask import request, session

from app import app
from app.utils import write_log


def logging(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if request.method in ('POST', 'PUT', 'PATHC'):
            payload = dict(request.form)
            if not payload:
                payload = request.json
        else:
            payload = dict(request.args)
        
        data = {
            'datetime': datetime.now(),
            'ip': request.remote_addr,
            'target_url': request.url,
            'cookies': request.cookies.get('session', '-'),
            'user_id': session.get('user_id', 'Anon'),
            'role_id': session.get('role', 'Anon'),
            'method': request.method,
            'payload': payload,
        }
        write_log(data)
        return f(*args, **kwargs)
    return inner
