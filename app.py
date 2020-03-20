import psycopg2
import qrcode
from flask import Flask, render_template, request ,redirect, url_for,session, flash
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from forms import *

app = Flask (__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:michael@localhost/uea_attendance'
app.config['SECRET_KEY'] = 'TEST'
app.debug=True

connection = psycopg2.connect(user="postgres", password="michael",
                                  host="localhost", port="5432", database="uea_attendance")

@app.route('/')
def index():
    if 'userID' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', title='Home')

@app.route('/register')
def regpage():
    form= RegisterForm()
    return render_template('register.html', title='Register', form=form)

@app.route('/registeruser', methods=['POST'])
def registerattempt():
    form = RegisterForm(request.form)
    if request.method== 'POST' and form.validate():
        cursor = connection.cursor()
        username= request.form['username']
        password= request.form['password']
        confirmpassword = request.form['confirmpassword']
        if password != confirmpassword:
            error = "Please check that passwords match"
            return render_template('register.html',title='Register', form=form, error=error)
        cursor.execute("INSERT INTO ueausers (username,password) VALUES (%s, %s)",
        (username,password))
        connection.commit()
        flash('User has been created')
        return redirect(url_for('loadlogin'))

@app.route('/login')
def loadlogin():
    if 'userID' in session:
        return render_template('dashboard.html')
    else:
        form = LoginForm()
        return render_template('login.html', title='Login', form=form)

@app.route('/loginattempt', methods=['POST'])
def loginattempt():
    form = LoginForm(request.form)
    if request.method== 'POST' and form.validate():
        cursor = connection.cursor()
        username= request.form['username']
        password= request.form['password']
        cursor.execute("SELECT * FROM ueausers where ueausers.username=%s and ueausers.password=%s",
        (username,password))
        found = cursor.fetchone()
        if found == None:
            error = "Invalid Credentials , Try Again"
            return render_template ("login.html", title='Login', form=LoginForm(), error = error)
            '''CODE BELOW NEEDS TO BE LOOKED AT AND REWORKED'''
        elif found[3] == 'admin':
            session['loggedIn'] = True
            session['userID'] = found[0]
            session['username'] = username
            session['accounttype'] = 'ADMIN'
            return redirect(url_for('admin'))
        elif found[3] == 'staff':
            session['loggedIn'] = True
            session['userID'] = found[0]
            session['username'] = username
            session['accounttype'] = 'STAFF'
            return redirect(url_for('dashboard'))
        else:
            session['accounttype'] = 'STUDENT'
            return redirect(url_for('dashboard'))



@app.route('/dashboard')
def dashboard():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM uealectures where staff_id= %s", (session['userID'],))
    found = cursor.fetchall()
    if found == None:
        return render_template('dashboard.html', title='Dashboard')
    else:
        return render_template('dashboard.html', title='Dashboard',data=found)

@app.route('/admin')
def admin():
    return render_template('dashboard.html', title="ADMIN Dashboard")

@app.route('/newlecture')
def newlecture():
    form = NewLectureForm()
    return render_template('newlecture.html', title='New Lecture', form=form)

@app.route('/feedback')
def feedback():
    return render_template('feedback.html', title='Feedback')

@app.route('/viewfeedback')
def viewfeedback():
    return render_template('viewfeedback.html', title='View Feedback')

@app.route('/createlecture', methods=['POST'])
def createlecture():
    form = NewLectureForm(request.form)
    if request.method== 'POST' and form.validate():
        cursor = connection.cursor()
        lecturename= form.lecturename.data
        lecturedate= form.lecturedate.data
        lecturetime= form.lecturetime.data
        cursor.execute("INSERT INTO uealectures (lecture_name, lecturedate, lecturetime, staff_id) VALUES (%s , %s, %s, %s)",
        (lecturename,lecturedate,lecturetime,session['userID']))
        connection.commit()
        flash('You have sucessfully added the lecture')
        return redirect(url_for('dashboard'))
    else:
        error=('Something has gone wrong')
        return render_template('newlecture.html', title='New Lecture', form=form, error=error)

@app.route('/editlecture/<string:id>', methods=['GET', 'POST'])
def edit_lecture(id):
        # Create cursor
        cursor = connection.cursor()

        # Get lecture by id
        result = cursor.execute("SELECT * FROM uealectures WHERE lecture_id = %s", [id])

        lecture = cursor.fetchone()
        # Get form
        form = NewLectureForm(request.form)
        # Populate lecture form fields
        form.lecturename.data = lecture[0]
        form.lecturedate.data = lecture[1]
        form.lecturetime.data = lecture[2]

        if request.method == 'POST' and form.validate():
            cursor = connection.cursor()
            lecturename= request.form['lecturename']
            lecturedate= request.form['lecturedate']
            lecturetime= request.form['lecturetime']
            cursor.execute("UPDATE uealectures SET lecture_name=%s, lecturedate=%s, lecturetime=%s WHERE lecture_id=%s",(lecturename,lecturedate,lecturetime,id))
            connection.commit()
            flash('You have sucessfully updated the lecture')
            return redirect(url_for('dashboard'))

        return render_template ('editlecture.html', form=form)


@app.route('/logout')
def logout():
    session.pop('userID')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
