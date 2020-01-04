from flask import Blueprint
from flask import Flask, redirect, url_for, request, render_template  # pip install flask
from flask_cors import CORS
from flask_api import status
import sys
import datetime as dt
import datedelta as dd
import numpy as np
import holidays
import sqlite3

from api.db import get_db

bp = Blueprint("reports", __name__)

hours_by_day = 10.5
weekmask_list = [1,1,0,1,1,0,0]
salary_month_net = 637
fees_day_net = 3.08

@bp.route("/reports/<int:year>/<int:month>")
def getBusinessDays(year, month):
    select_start = str(year)+str(month)+"01"
    select_end_tmp = dt.date(year, month, 1) + dd.datedelta(months=1)
    select_end = select_end_tmp.strftime('%Y%m%d')
    db = get_db()
    data = db.execute("select day from days_off where day >= " + select_start + " and day < " + select_end ).fetchall()
    db.close()

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

