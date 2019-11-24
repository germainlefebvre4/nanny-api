import sys
import sqlite3
import mysql.connector as mariadb

## SQLite3
#DATABASE_NAME = "nanny.db"
#conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
#app = Flask(__name__)
#c = conn.cursor()
#c.execute('''CREATE TABLE days_exception (creation text, exception text)''')
#c.close()

# MariaDB
conn = mariadb.connect(host='localhost:3307', user='root', password='', database='nanny')
cursor = conn.cursor()
c.execute('''CREATE TABLE days_exception (creation text, exception text)''')
c.close()

