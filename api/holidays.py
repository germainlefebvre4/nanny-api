'''
from flask import Blueprint
from flask import Flask, redirect, url_for, request, render_template, jsonify
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

bp = Blueprint("holidays", __name__, url_prefix="/api")

@bp.route("/holidays")
def getHolidaysByMonth():
    year = request.args.get('year', default=None, type=int)
    month = request.args.get('month', default=None, type=int)

    if year and not month:
        holidays_fra = [dict(day=dt.datetime.strftime(x[0], "%Y-%m-%d")) for x in holidays.FRA(years=year).items()]
    elif year and month:
        holidays_fra = [dict(day=dt.datetime.strftime(x[0], "%Y-%m-%d")) for x in holidays.FRA(years=year).items() if dt.datetime.strftime(x[0], "%m") == "{:02}".format(month)]
    
    return jsonify(holidays_fra)
'''