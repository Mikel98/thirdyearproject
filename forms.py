from flask_wtf import Form
from wtforms import Form, StringField, PasswordField,DateField, DateTimeField, IntegerField,SubmitField,SelectField
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
    lecturecode = StringField('Lecture Code:')
    submit = SubmitField('Create Lecture')

class UpdateLectureForm(Form):
    lecturename = StringField('Lecture Name:', [validators.DataRequired()])
    lecturedate = DateField('Lecture Date:', [validators.DataRequired()])
    lecturetime = TimeField('Lecture Time:', [validators.DataRequired()])
    lecturecode = StringField('Lecture Code:')
    submit = SubmitField('Update Lecture')

class StaffPersonalForm(Form):
    forename = StringField('Forename:', [validators.DataRequired()])
    surname = StringField('Surname:', [validators.DataRequired()])
    email = StringField('Email Address:', [validators.DataRequired()])
    faculty = SelectField('Faculty',choices=[('A&H','Arts & Humanities'), ('M&HS','Medicine & Health Sciences'),('S','Science'),('SS','Social Sciences')])
    submit = SubmitField('Update Details')

class AttendanceForm(Form):
        lecture_id=IntegerField()
        student_id=IntegerField()
        forename = StringField('Forename:', [validators.DataRequired()])
        surname = StringField('Surname:', [validators.DataRequired()])
        attendance = StringField()
        submit = SubmitField('Register Attendance')

class FeedbackForm(Form):
    lecturecode = StringField('Lecture Code:', [validators.DataRequired()])
    feedback = StringField()
    submit = SubmitField('Give Feedback')
