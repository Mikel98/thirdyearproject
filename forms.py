from flask_wtf import Form
from wtforms import Form, StringField, PasswordField,DateField, DateTimeField, IntegerField,SubmitField
from wtforms import validators, ValidationError
from wtforms_components import TimeField
from wtforms.fields.html5 import DateField

class RegisterForm(Form):
    username = StringField('Enter Username: ', [validators.DataRequired()])
    password = PasswordField('Enter Password: ', [validators.DataRequired()])
    confirmpassword = PasswordField('Confirm Password: ', [validators.DataRequired()])
    submit= SubmitField('Register')

class LoginForm(Form):
    username = StringField('Username:', [validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired()])
    submit= SubmitField('Login')

class NewLectureForm(Form):
    lecturename = StringField('Lecture Name:', [validators.DataRequired()])
    lecturedate = DateField('Lecture Date:', [validators.DataRequired()])
    lecturetime = TimeField('Lecture Time:', [validators.DataRequired()])
    submit = SubmitField('Create Lecture')
