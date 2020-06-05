**Lecture and Attendance Feedback System**

Third Year Computer Science project using web technologies
Technologies used:
- HTML
- CSS
- JavaScript
- Python
- Postgres

----------

Install dependencies
> pip install virtualenv (name your virtual environment here)

> activate virtualenv

>pip install requirements.txt

----------

Pre requisites


To link the database with the system Postgres must be installed. Open the client and create a new database titled "uea_attendance". Once this has been done open the database then schema and right click on public. A menu will appear and select Query Tool. Once the tool opens click the open folder button in the top left and navigate to the database.sql file associated with this project. Confirm the choice and then click the play button in the query tool. The database should now fill with all the required tables

In addition ,to maximise functionality of this system the use of a localhost server is required. It is important to find the ipv4 address of the machine this system will be run on and then update the app.host within the app.py file and also paste the ipv4 address within the lectureCodes.html files qr code address

----------
To Run

>python .\app.py
>follow instructions displayed within the command line
