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
    lecturename = StringField('Session Name:', [validators.DataRequired()])
    sessiondate = DateField('Session Date:', [validators.DataRequired()])
    sessiontime = TimeField('Session Time:', [validators.DataRequired()])
    lecturecode = StringField('Session Code:')
    sessiontype = SelectField('Session Type:',choices=[('Lec','Lecture'), ('Sem','Seminar'),('Lab','Lab')])
    submit = SubmitField('Create Session')

class UpdateLectureForm(Form):
    session_name = StringField('Session Name:', [validators.DataRequired()])
    sessiondate = DateField('Session Date:', [validators.DataRequired()])
    sessiontime = TimeField('Session Time:', [validators.DataRequired()])
    sessioncode = StringField('Session Code:')
    sessiontype = SelectField('Session Type:',choices=[('Lec','Lecture'), ('Sem','Seminar'),('Lab','Lab')])
    submit = SubmitField('Update Session')

class StaffPersonalForm(Form):
    forename = StringField('Forename:', [validators.DataRequired()])
    surname = StringField('Surname:', [validators.DataRequired()])
    email = StringField('Email Address:', [validators.DataRequired()])
    faculty = SelectField('Faculty',choices=[('A&H','Arts & Humanities'), ('M&HS','Medicine & Health Sciences'),('S','Science'),('SS','Social Sciences')])
    submit = SubmitField('Update Details')

class StudentPersonalForm(Form):
    forename = StringField('Forename:', [validators.DataRequired()])
    surname = StringField('Surname:', [validators.DataRequired()])
    email = StringField('Email Address:', [validators.DataRequired()])
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
