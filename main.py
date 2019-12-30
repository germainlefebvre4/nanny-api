from flask import Flask, redirect, url_for, request, render_template  # pip install flask
from flask_cors import CORS
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
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/.*": {"origins": "http://localhost"}})

# c = conn.cursor()
# c.execute('''CREATE TABLE days_exception (creation text, exception text)''')
# c.close()

hours_by_day = 10.5
weekmask_list = [1,1,0,1,1,0,0]
salary_month_net = 637
fees_day_net = 3.08

@app.route("/reports/<int:year>/<int:month>")
def getBusinessDays(year, month):
    select_start = str(year)+str(month)+"01"
    select_end_tmp = dt.date(year, month, 1) + dd.datedelta(months=1)
    select_end = select_end_tmp.strftime('%Y%m%d')
    c = conn.cursor()
    c.execute("select exception from days_exception where exception >= " + select_start + " and exception < " + select_end )
    data = c.fetchall()
    c.close()

    days_exception = [dt.date(int(x[0][:4]), int(x[0][4:-2]), int(x[0][-2:])) for x in data]

    start = dt.date( year, month, 1 )
    end = dt.date(year, month, 1) + dd.datedelta(months=1)
    holidays_fra = [x[0] for x in holidays.FRA(years=year).items()]
    bdays = int(np.busday_count( start, end , weekmask=weekmask_list, holidays=holidays_fra ))
    bdays_wExceptions = int(np.busday_count( start, end , weekmask=weekmask_list, holidays=holidays_fra+days_exception ))
    hours_normalByMonth = int(hours_by_day*weekmask_list.count(1)*52/12)
    month_str = dt.date(year, month, 1).strftime("%B")
    fees_month_net = "{0:.2f}".format(fees_day_net*bdays_wExceptions)
    return {
            "year": year,
            "month": month_str,
            "monthId": month,
            "businessDays": bdays,
            "businessDaysWithExceptions": bdays_wExceptions,
            "normalHours": hours_normalByMonth,
            "salary": salary_month_net,
            "fees": fees_month_net
    }

@app.route("/calendar/exceptions", methods=["GET"])
def getBusinessDayException():
    c = conn.cursor()
    c.execute("select * from days_exception")
    data = c.fetchall()
    c.close()
    return json.dumps(data)

@app.route("/calendar/exceptions", methods=["POST"])
def addBusinessDayException():
    creation = dt.datetime.now()
    day = request.form.get("day")
    month = request.form.get("month")
    year = request.form.get("year")
    exception = "{}{}{}".format(year, month, day) # dt.date( year, month, day )

    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO days_exception(creation,exception) VALUES (?,?)', (creation, exception))
    conn.commit()
    c.close()
    return { "msg": "Day {}-{}-{} added to day exceptions.".format(day, month, year) }, status.HTTP_201_CREATED

@app.route("/calendar/exceptions", methods=["DELETE"])
def delBusinessDayException():
    creation = dt.datetime.now()
    day = request.form.get("day")
    month = request.form.get("month")
    year = request.form.get("year")
    exception = "{}{}{}".format(year, month, day) # dt.date( year, month, day )

    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM days_exception WHERE exception = ?', [exception])
    conn.commit()
    c.close()
    return { "msg": "Day {}-{}-{} removed from day exceptions.".format(day, month, year) }, status.HTTP_201_CREATED


@app.route("/")
def getProducts():
    links = [
        "/reports/2019/10",
        "/calendar/exceptions"
    ]
    return render_template('doc.html', links=links)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
