import psycopg2
import qrcode
import random
import string
from flask import Flask, render_template, request ,redirect, url_for,session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from functools import wraps
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
from forms import *

def randomString(stringLength=20):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

app = Flask (__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:michael@localhost/uea_attendance'
app.config['SECRET_KEY'] = randomString()
app.permanent_session_lifetime = timedelta(minutes=5)
app.debug=True
QRcode(app)
connection = psycopg2.connect(user="postgres",password="michael",host="localhost",port="5432",database="uea_attendance")
