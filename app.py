import psycopg2
import qrcode
from flask import Flask, render_template, request ,redirect, url_for,session, flash
from flask_sqlalchemy import SQLAlchemy

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
        return render_template('dashboard.html')
    else:
        return render_template('index.html', title='Home')

@app.route('/login')
def loadlogin():
    if 'userID' in session:
        return render_template('dashboard.html')
    else:
        return render_template('login.html', title='Login')

@app.route('/loginattempt', methods=['POST'])
def loginattempt():
    cursor = connection.cursor()
    username= request.form['username']
    password= request.form['password']
    cursor.execute("SELECT * FROM ueausers where ueausers.username=%s and ueausers.password=%s",
    (username,password))
    found = cursor.fetchone()
    if found == None:
        error = "Invalid Credentials , Try Again"
        return render_template ("login.html", title='Login', error = error)
    else:
        session['loggedIn'] = True
        session['userID'] = found[0]
        session['username'] = username
        return redirect(url_for('dashboard'))



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route('/newlecture')
def newlecture():
    return render_template('newlecture.html', title='New Lecture')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html', title='Feedback')

@app.route('/viewfeedback')
def viewfeedback():
    return render_template('viewfeedback.html', title='View Feedback')

@app.route('/createlecture', methods=['POST'])
def createlecture():
    cursor = connection.cursor()
    lecturename= request.form['lecture_name']
    lecturedate= request.form['lecture_Date']
    lecturetime= request.form['lecutre_Time']
    staff_id=request.form['staff_ID']
    cursor.execute("INSERT INTO uealectures (lecture_name, lecturedate, lecturetime, staff_id) VALUES (%s , %s, %s, %s)",
    (lecturename,lecturedate,lecturetime,staff_id))
    connection.commit()
    flash('You have sucessfully added the lecture')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('userID')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
