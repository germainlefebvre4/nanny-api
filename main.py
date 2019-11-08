from flask import Flask, redirect, url_for, request, render_template  # pip install flask
from flask_api import status
import sys
import datetime as dt
import datedelta as dd
import numpy as np
import holidays
import sqlite3
import json

DATABASE_NAME = "nanny.db"
conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
app = Flask(__name__)
# c = conn.cursor()
# c.execute('''CREATE TABLE days_exception (creation text, exception text)''')
# c.close()

salary_month_net = 367
fees_day_net = 3.08

@app.route("/business/month/<int:year>/<int:month>")
def getBusinessDays(year, month):
   start = dt.date( year, month, 1 )
   end = dt.date(year, month, 1) + dd.datedelta(months=1)
   holidays_fra = [x[0] for x in holidays.FRA(years=2019).items()]
   bdays = int(np.busday_count( start, end , weekmask=[1,1,0,1,1,0,0], holidays=holidays_fra ))
   month_str = dt.date(year, month, 1).strftime("%B")
   fees_month_net = fees_day_net*bdays
   return  {month_str: {"businessDays": bdays, "salary": salary_month_net, "fees": fees_month_net }}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
