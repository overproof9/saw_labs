from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    passwd = db.Column(db.String(150), nullable=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.set_password(kwargs.get('passwd', None))

    def set_password(self, row_password):
        self.passwd = generate_password_hash(row_password)

    def check_password(self, password):
        return check_password_hash(self.passwd, password)
    
    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(140), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Post {self.id}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('comments', lazy=True)) 
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Post {self.id}>"
