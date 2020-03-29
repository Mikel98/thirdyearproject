import psycopg2
import qrcode
import random
import string
from flask import Flask, render_template, request ,redirect, url_for,session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from passlib.hash import sha256_crypt
from forms import *

global lecture_IDENTITY
def randomString(stringLength=20):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def randomLectureCode(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

app = Flask (__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:michael@localhost/uea_attendance'
app.config['SECRET_KEY'] = randomString()
app.debug=True
QRcode(app)
connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")

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
        connection.close()
        flash('User has been created', 'success')
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
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
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
        elif found[3] == 'admin':
            session['loggedInAdmin'] = True
            session['userID'] = found[0]
            session['username'] = username
            session['accounttype'] = 'ADMIN'
            flash('You are now logged in', 'success')
            return redirect(url_for('admin'))
        elif found[3] == 'staff':
            session['loggedInStaff'] = True
            session['userID'] = found[0]
            session['username'] = username
            session['accounttype'] = 'STAFF'
            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            session['loggedInStudent'] = True
            session['userID'] = found[0]
            session['username'] = username
            session['accounttype'] = 'STUDENT'
            connection.close()
            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM uealectures where staff_id= %s", (session['userID'],))
    found = cursor.fetchall()
    connection.close()
    if found == None:
        return render_template('dashboard.html', title='Dashboard')
    else:
        return render_template('dashboard.html', title='Dashboard',data=found)

@app.route('/admin')
def admin():
    return render_template('dashboard.html', title="ADMIN Dashboard")

@app.route('/staffupdatedetails', methods=['GET'])
def staffupdatedetails():
        connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
        cursor = connection.cursor()
        # Get staff member by id
        cursor.execute("SELECT * FROM ueastaff WHERE staff_id = %s", (session['userID'],))
        found = cursor.fetchone()
            # Get form
        form = StaffPersonalForm()
            # Populate lecture form fields
        form.forename.data = found[1]
        form.surname.data = found[2]
        form.email.data = found[3]
        form.faculty.data = found[4]
        connection.close()
        return render_template('updatedetails.html', title='Update Details', form=form)

@app.route('/staffdetailspush', methods=['POST'])
def detailsupdateattempt():
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    cursor = connection.cursor()
    form = StaffPersonalForm(request.form)
    if request.method== 'POST' and form.validate():
        cursor = connection.cursor()
        forename= form.forename.data
        surname= form.surname.data
        email= form.email.data
        faculty= form.faculty.data
        cursor.execute("UPDATE ueastaff SET staff_forename=%s, staff_surname=%s, staff_email=%s, staff_faculty=%s WHERE staff_id=%s",(forename,surname,email, faculty,session['userID']))
        connection.commit()
        connection.close()
        flash('Details have been updated', 'success')
        return redirect(url_for('dashboard'))

@app.route('/newlecture')
def newlecture():
    form = NewLectureForm()
    return render_template('newlecture.html', title='New Lecture', form=form)

@app.route('/createlecture', methods=['POST'])
def createlecture():
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    form = NewLectureForm(request.form)
    if request.method== 'POST' and form.validate():
        cursor = connection.cursor()
        lecturename= form.lecturename.data
        lecturedate= form.lecturedate.data
        lecturetime= form.lecturetime.data
        lecturecode= randomLectureCode()
        cursor.execute("INSERT INTO uealectures (lecture_name, lecturedate, lecturetime, staff_id,lecture_code) VALUES (%s , %s, %s, %s, %s)",
        (lecturename,lecturedate,lecturetime,session['userID'],lecturecode))
        connection.commit()
        connection.close()
        flash('You have sucessfully added the lecture', 'success')
        return redirect(url_for('dashboard'))
    else:
        error=('Something has gone wrong')
        return render_template('newlecture.html', title='New Lecture', form=form, error=error)

@app.route('/editlecture/<string:id>', methods=['GET', 'POST'])
def edit_lecture(id):
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
        # Create cursor
    cursor = connection.cursor()

        # Get lecture by id
    result = cursor.execute("SELECT * FROM uealectures WHERE lecture_id = %s", [id])

    lecture = cursor.fetchone()
        # Get form
    form = UpdateLectureForm(request.form)
        # Populate lecture form fields
    form.lecturename.data = lecture[0]
    form.lecturedate.data = lecture[1]
    form.lecturetime.data = lecture[2]
    form.lecturecode.data = lecture[5]

    if request.method == 'POST' and form.validate():
        cursor = connection.cursor()
        lecturename= request.form['lecturename']
        lecturedate= request.form['lecturedate']
        lecturetime= request.form['lecturetime']
        cursor.execute("UPDATE uealectures SET lecture_name=%s, lecturedate=%s, lecturetime=%s WHERE lecture_id=%s",(lecturename,lecturedate,lecturetime,id))
        connection.commit()
        connection.close()
        flash('You have sucessfully updated the lecture', 'success')
        return redirect(url_for('dashboard'))

    return render_template ('editlecture.html', form=form)

@app.route('/deletelecture/<string:id>', methods=['POST'])
def deletelecture(id):
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    cur = connection.cursor()
    # Delete Lecture by id
    cur.execute("DELETE FROM uealectures WHERE lecture_id = %s", [id])
    connection.commit()
    connection.close()
    flash('Lecture Deleted', 'success')
    return redirect(url_for('dashboard'))

@app.route('/registerattendance/<string:id>', methods=['GET', 'POST'])
def registerattendance(id):
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    cur = connection.cursor()
    # Delete Lecture by id
    flash('Lecture Deleted', 'success')
    return render_template("dashboard.html", title="REG DASH")

@app.route('/lecturecodes/<string:id>', methods= ['GET'])
def lecturecodes(id):
    global lecture_IDENTITY
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    # Create cursor
    cursor = connection.cursor()
    # Get lecture by id
    result = cursor.execute("SELECT * FROM uealectures WHERE lecture_id = %s", [id])
    lecture = cursor.fetchone()
    lectureid = lecture[4]
    lecture_IDENTITY = lecture[4]
    return render_template('lecturecodes.html', title='Lecture Codes', data=lecture)

@app.route('/attregister',methods=['GET','POST'])
def register():
    global lecture_IDENTITY
    form=AttendanceForm(request.form)
    return redirect(url_for('attemptreg'))


@app.route('/regattendance',methods=['GET','POST'])
def attemptreg():
    lecture_IDENTITY
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    # Create cursor
    cursor = connection.cursor()
    # Get lecture by id
    form = AttendanceForm()
    result = cursor.execute("SELECT * FROM uealectures WHERE lecture_id = %s", [lecture_IDENTITY])
    lecture = cursor.fetchone()
        # Get form
    form= AttendanceForm(request.form)
        # Populate lecture form fields
    form.lecture_id.data = lecture_IDENTITY
    form.student_id.data= 1
    return render_template('attreg.html', title='Register', form=form)

@app.route('/lecturefeedback')
def feedbackload():
    form = FeedbackForm()
    return render_template('submitfeedback.html', title='Lecture Feedback', form=form)

@app.route('/sendfeedback', methods=['POST'])
def sendfeedback():
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    # Create cursor
    form = FeedbackForm(request.form)
    if request.method== 'POST' and form.validate():
        cursor = connection.cursor()
        lecture_code= request.form['lecturecode']
        feedback= request.form['feedback']
        cursor.execute("INSERT INTO ueafeedback (lecture_code,feedback) VALUES (%s, %s)",
        (lecture_code,feedback))
        connection.commit()
        connection.close()
        flash('Feedback has been submited', 'success')
        return redirect(url_for('index'))

@app.route('/viewfeedback/<string:id>', methods=['GET', 'POST'])
def viewfeedback(id):
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
        # Create cursor
    cursor = connection.cursor()

        # Get feedback by code
    result = cursor.execute("SELECT uealectures.lecture_id,uealectures.lecture_name, ueafeedback.lecture_code, ueafeedback.feedback FROM ueafeedback INNER JOIN uealectures ON ueafeedback.lecture_code=uealectures.lecture_code WHERE ueafeedback.lecture_code =%s",[id])
    found = cursor.fetchall()
    connection.close()
    if found == None:
        error = "No Feedback has been submitted yet"
        return render_template('dashboard.html', title='Dashboard', error=error)
    else:
        return render_template('viewfeedback.html', title='View Feedback',data=found)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    lecture_IDENTITY = None
    app.run(host='192.168.0.141')
