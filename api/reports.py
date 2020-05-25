from flask import Blueprint
from flask import Flask, redirect, url_for, request, render_template  # pip install flask
from flask_cors import CORS
from flask_api import status
from flask import current_app
# import logging
import sys
import datetime as dt
import datedelta as dd
import numpy as np
import holidays
import sqlite3

from api.db import get_db

bp = Blueprint("reports", __name__, url_prefix="/api")

hours_by_day = 10.5
weekmask_list = [1,1,0,1,1,0,0]
# salary_month_net = 637
salary_hour_net = 3.50
fees_day_net = 3.08

@bp.route("/reports/<int:year>/<int:month>")
def getReport(year, month):
    select_start = "{:04d}-{:02d}-{:02d}".format(int(year), int(month), 1) # str(year)+str(month)+"01"
    select_end_tmp = dt.date(year, month, 1) + dd.datedelta(months=1)
    select_end = select_end_tmp.strftime('%Y-%m-%d')
    current_app.logger.info("Dearch dates: From {} to {}".format(select_start, select_end))

    # DB queries
    db = get_db()
    
    cur = db.cursor()
    absence_child_rows = cur.execute("select day from days_off where absenceid = ? and day >= ? and day < ?", [1, select_start, select_end] ).fetchall()
    absence_child = []
    for absence_child_row in absence_child_rows:
        [current_app.logger.info(x) for x in absence_child_row]
        [absence_child.append(dt.date(int(x[:4]), int(x[5:-3]), int(x[-2:]))) for x in absence_child_row]
    current_app.logger.info(absence_child)

    disease_child_rows = db.execute("select day from days_off where absenceid = ? and day >= ? and day < ?", [2, select_start, select_end] ).fetchall()
    disease_child = []
    for disease_child_row in disease_child_rows:
        [disease_child.append(dt.date(int(x[:4]), int(x[5:-3]), int(x[-2:]))) for x in disease_child_row]
    current_app.logger.info(disease_child)
    
    dayoff_nanny_rows = db.execute("select day from days_off where absenceid = ? and day >= ? and day < ?", [3, select_start, select_end] ).fetchall()
    dayoff_nanny = []
    for dayoff_nanny_row in dayoff_nanny_rows:
        [dayoff_nanny.append(dt.date(int(x[:4]), int(x[5:-3]), int(x[-2:]))) for x in dayoff_nanny_row]
    current_app.logger.info(dayoff_nanny)

    disease_nanny_rows = db.execute("select day from days_off where absenceid = ? and day >= ? and day < ?", [4, select_start, select_end] ).fetchall()
    disease_nanny = []
    for disease_nanny_row in disease_nanny_rows:
        [disease_nanny.append(dt.date(int(x[:4]), int(x[5:-3]), int(x[-2:]))) for x in disease_nanny_row]
    current_app.logger.info(disease_nanny)
    db.close()



    start = dt.date( year, month, 1 )
    end = dt.date(year, month, 1) + dd.datedelta(months=1)
    holidays_fra = [x[0] for x in holidays.FRA(years=year).items()]
    current_app.logger.info(holidays_fra+dayoff_nanny+disease_nanny+absence_child+disease_child)

    month_str = dt.date(year, month, 1).strftime("%B")
    bdays = int(np.busday_count( start, end , weekmask=weekmask_list, holidays=holidays_fra ))
    bdays_salary_wExceptions = int(np.busday_count( start, end , weekmask=weekmask_list, holidays=holidays_fra+disease_nanny+disease_child ))
    bdays_fees_wExceptions = int(np.busday_count( start, end , weekmask=weekmask_list, holidays=holidays_fra+dayoff_nanny+disease_nanny+absence_child+disease_child ))
    hours_normalByMonth = int(hours_by_day*weekmask_list.count(1)*52/12)
    fees_month_net = "{0:.2f}".format(fees_day_net*bdays_fees_wExceptions)
    salary_month_net = "{0:.2f}".format(salary_hour_net*hours_by_day*sum(weekmask_list)*52/12*bdays_salary_wExceptions/bdays)
    
    return {
        "year": year,
        "month": month_str,
        "monthId": month,
        "businessDays": bdays,
        "businessDaysForSalary": bdays_salary_wExceptions,
        "businessDaysForFees": bdays_fees_wExceptions,
        "normalHours": hours_normalByMonth,
        "salary": salary_month_net,
        "fees": fees_month_net
    }


