from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    email = StringField('Email')
    username = StringField('Username')
    password1 = PasswordField('Password')
    password2 = PasswordField('Repeat Password')
    submit = SubmitField('Register')


class PostForm(FlaskForm):
    title = StringField('Title')
    body = StringField('Body')
    submit = SubmitField('Post!')


