from modules import *

global lecture_IDENTITY

def randomLectureCode(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

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
        hashedpassword =  sha256_crypt.hash(password)
        if password != confirmpassword:
            error = "Please check that passwords match"
            return render_template('register.html',title='Register', form=form, error=error)
        cursor.execute("INSERT INTO ueausers (username,password) VALUES (%s, %s)",
        (username,hashedpassword))
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
        cursor.execute("SELECT * FROM ueausers where username=%s", (username,))
        found = cursor.fetchone()
        if sha256_crypt.verify(password, found[2]) and found[3] == 'admin':
            session['loggedInAdmin'] = True
            session['userID'] = found[0]
            session['username'] = username
            session['accounttype'] = 'ADMIN'
            flash('You are now logged in', 'success')
            return redirect(url_for('admin'))
        elif sha256_crypt.verify(password, found[2]) and found[3] == 'staff':
            session['loggedInStaff'] = True
            session['userID'] = found[0]
            session['username'] = username
            session['accounttype'] = 'STAFF'
            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        elif sha256_crypt.verify(password, found[2]):
            session['loggedInStudent'] = True
            session['userID'] = found[0]
            session['username'] = username
            session['accounttype'] = 'STUDENT'
            connection.close()
            flash('You are now logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid Credentials , Try Again"
            return render_template ("login.html", title='Login', form=LoginForm(), error = error)

@app.route('/dashboard')
def dashboard():
    if 'userID' in session:
        connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ueasession where staff_id= %s", (session['userID'],))
        found = cursor.fetchall()
        connection.close()
        if found == None:
            return render_template('dashboard.html', title='Dashboard')
        else:
            return render_template('dashboard.html', title='Dashboard',data=found)
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/admin')
def admin():
    if 'loggedInAdmin' in session:
        return render_template('admindashboard.html', title="ADMIN Dashboard")
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/staffupdatedetails', methods=['GET'])
def staffupdatedetails():
    if 'loggedInStaff' in session:
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
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/staffdetailspush', methods=['POST'])
def detailsupdateattempt():
    if 'loggedInStaff' in session:
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
        else:
            error = 'Please Log In'
            return render_template('index.html', title='Home',error=error)

@app.route('/newlecture')
def newlecture():
    if 'loggedInStaff' in session:
        form = NewLectureForm()
        return render_template('newlecture.html', title='New Lecture', form=form)
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/createlecture', methods=['POST'])
def createlecture():
    if 'loggedInStaff' in session:
        connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
        form = NewLectureForm(request.form)
        if request.method== 'POST' and form.validate():
            cursor = connection.cursor()
            lecturename= form.lecturename.data
            sessiondate= form.sessiondate.data
            sessiontime= form.sessiontime.data
            lecturecode= randomLectureCode()
            session_type = form.sessiontype.data
            cursor.execute("INSERT INTO ueasession (session_name, sessiondate, sessiontime, staff_id, lecture_code, session_type) VALUES (%s , %s, %s, %s, %s,%s)",
            (lecturename,sessiondate,sessiontime,session['userID'],lecturecode, session_type))
            connection.commit()
            connection.close()
            flash('You have sucessfully added the lecture', 'success')
            return redirect(url_for('dashboard'))
        else:
            error=('Something has gone wrong')
            return render_template('newlecture.html', title='New Lecture', form=form, error=error)
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/editlecture/<string:id>', methods=['GET', 'POST'])
def edit_lecture(id):
    if 'loggedInStaff' in session:
        connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
            # Create cursor
        cursor = connection.cursor()

            # Get lecture by id
        result = cursor.execute("SELECT * FROM ueasession WHERE lecture_id = %s", [id])

        lecture = cursor.fetchone()
            # Get form
        form = UpdateLectureForm(request.form)
            # Populate lecture form fields
        form.lecturename.data = lecture[0]
        form.sessiondate.data = lecture[1]
        form.sessiontime.data = lecture[2]
        form.lecturecode.data = lecture[5]

        if request.method == 'POST' and form.validate():
            cursor = connection.cursor()
            lecturename= request.form['lecturename']
            sessiondate= request.form['sessiondate']
            sessiontime= request.form['sessiontime']
            cursor.execute("UPDATE ueasession SET session_name=%s, sessiondate=%s, sessiontime=%s WHERE lecture_id=%s",(lecturename,sessiondate,sessiontime,id))
            connection.commit()
            connection.close()
            flash('You have sucessfully updated the lecture', 'success')
            return redirect(url_for('dashboard'))
        return render_template ('editlecture.html', form=form)
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/deletelecture/<string:id>', methods=['POST'])
def deletelecture(id):
    if 'loggedInStaff' in session:
        connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
        cur = connection.cursor()
        # Delete Lecture by id
        cur.execute("DELETE FROM ueasession WHERE lecture_id = %s", [id])
        connection.commit()
        connection.close()
        flash('Lecture Deleted', 'success')
        return redirect(url_for('dashboard'))
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/lecturecodes/<string:id>', methods= ['GET'])
def lecturecodes(id):
    if 'loggedInStaff' in session:
        global lecture_IDENTITY
        connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
        # Create cursor
        cursor = connection.cursor()
        # Get lecture by id
        result = cursor.execute("SELECT * FROM ueasession WHERE lecture_id = %s", [id])
        lecture = cursor.fetchone()
        lectureid = lecture[4]
        lecture_IDENTITY = lecture[4]
        return render_template('lecturecodes.html', title='Lecture Codes', data=lecture)
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/attregister',methods=['GET','POST'])
def register():
    global lecture_IDENTITY
    return redirect(url_for('studentlogin'))

@app.route('/studentlogin', methods=['GET','POST'])
def studentlogin():
    global lecture_IDENTITY
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    form = LoginForm(request.form)
    return render_template('studentlogin.html', title= 'Student Login', form=form)

@app.route('/test', methods=['POST'])
def test():
    global lecture_IDENTITY
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    form = LoginForm(request.form)
    if request.method== 'POST' and form.validate():
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        username= request.form['username']
        password= request.form['password']
        hashedpassword =  sha256_crypt.hash(password)
        cursor.execute("SELECT * FROM ueausers where username=%s", (username,))
        found = cursor.fetchone()
        if sha256_crypt.verify(password, found[2]) and found[3] == 'student':
            session['loggedInStudent'] = True
            session['studentID'] = found[0]
            return redirect(url_for('attemptreg'))
        elif sha256_crypt.verify(password, found[2]) and found[3] != 'student':
            error = "Access Level Incorrect, Use different details"
            return render_template ("studentlogin.html", title='Student Login', form=LoginForm(), error = error)
        else:
            error = "Invalid Credentials , Try Again"
            return render_template ("studentlogin.html", title='Student Login', form=LoginForm(), error = error)
            connection.close()

@app.route('/regattendance',methods=['GET','POST'])
def attemptreg():
    lecture_IDENTITY
    connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
    # Create cursor
    cursor = connection.cursor()
    cursor2 = connection.cursor()
    # Get lecture by id
    form = AttendanceForm()
    result = cursor.execute("SELECT * FROM ueasession WHERE lecture_id = %s", [lecture_IDENTITY])
    test = cursor2.execute("SELECT ueastudent.student_id,ueastudent.student_forename, ueastudent.student_surname FROM ueastudent INNER JOIN ueausers ON ueausers.id=ueastudent.student_id WHERE ueastudent.student_id =%s",(session['studentID'],))
    lecture = cursor.fetchone()
    studentinfo = cursor2.fetchone()
        # Get form
    form= AttendanceForm(request.form)
        # Populate lecture form fields
    form.lecture_id.data = lecture_IDENTITY
    form.student_id.data= studentinfo[0]
    form.forename.data=studentinfo[1]
    form.surname.data=studentinfo[2]
    form.attendance.data='Present'
    return render_template('attreg.html', title='Register', form=form)

@app.route('/registerattendance', methods=['POST'])
def submitattendance():
    if 'loggedInStudent' in session:
        connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
        form = AttendanceForm(request.form)
        if request.method== 'POST' and form.validate():
            try:
                cursor = connection.cursor()
                lectureID= form.lecture_id.data
                studentID= form.student_id.data
                forename= form.forename.data
                surname= form.surname.data
                mark= form.attendance.data
                cursor.execute("INSERT INTO lectureattendance (lecture_id, student_id, student_forename, student_surname,attendance_mark) VALUES (%s , %s, %s, %s, %s)",
                (lectureID,studentID,forename,surname,mark))
                connection.commit()
                connection.close()
            except Exception as error:
                error=('Unable to register attendance, contact IT support')
                return render_template('index.html', title='Home', error=error)
            flash('You have sucessfully registered for this lecture', 'success')
            return redirect(url_for('index'))
        else:
            error=('Unable to register attendance, contact IT support')
            return render_template('index.html', title='Home', error=error)
    else:
        error='Access Credentials Invalid'
        return render_template('index.html', title='Home', error=error)


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
    if 'loggedInStaff' in session:
        connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
            # Create cursor
        cursor = connection.cursor()

            # Get feedback by code
        result = cursor.execute("SELECT ueasession.lecture_id,ueasession.session_name, ueafeedback.lecture_code, ueafeedback.feedback FROM ueafeedback INNER JOIN ueasession ON ueafeedback.lecture_code=ueasession.lecture_code WHERE ueafeedback.lecture_code =%s",[id])
        found = cursor.fetchall()
        connection.close()
        if found == None:
            error = "No Feedback has been submitted yet"
            return render_template('dashboard.html', title='Dashboard', error=error)
        else:
            return render_template('viewfeedback.html', title='View Feedback',data=found)
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/viewattendance/<string:id>', methods=['GET', 'POST'])
def viewattendance(id):
    if 'loggedInStaff' in session:
        connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
            # Create cursor
        cursor = connection.cursor()

            # Get feedback by code
        result = cursor.execute("SELECT * FROM (SELECT  lecture_id,CONCAT(student_forename, ' ', student_surname) AS student_name, attendance_mark FROM lectureattendance) base WHERE lecture_id =%s",[id])
        found = cursor.fetchall()
        connection.close()
        if found == None:
            error = "No Feedback has been submitted yet"
            return render_template('dashboard.html', title='Dashboard', error=error)
        else:
            return render_template('attendance.html', title='Lecture Attendance',data=found)
    else:
        error = 'Please Log In'
        return render_template('index.html', title='Home',error=error)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    lecture_IDENTITY = None
    app.run(host='192.168.0.21')
