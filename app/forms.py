from flask_wtf import FlaskForm as Form
from wtforms import StringField,PasswordField,TextAreaField,BooleanField
from wtforms.validators import InputRequired,Email,Length

class SignupForm(Form):
    email=StringField('email',validators=[InputRequired(),Email(message='Invalid email')])#error message for other fields too ?
    username=StringField('username',validators=[InputRequired()])#,Length(min=3)])
    password=PasswordField('password',validators=[InputRequired()])#,Length(min=7)])
    remember=BooleanField('remember')

class LoginForm(Form):
    username=StringField('username')
    password=PasswordField('password')
    remember=BooleanField('remember')

class AddProjectForm(Form):
    title=StringField('title')
    text=TextAreaField('text')
