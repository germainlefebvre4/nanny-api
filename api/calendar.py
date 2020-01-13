# coding: utf8

from flask import Blueprint
from flask import Flask, redirect, url_for, request, render_template  # pip install flask
from flask_cors import CORS
from flask_api import status
import json
import datetime as dt
import sqlite3

from api.db import get_db

bp = Blueprint("calendar", __name__)

@bp.route("/calendar/exceptions", methods=["GET"])
def getBusinessDayException():
    data = []

    db = get_db()
    cur = db.cursor()
    rows = cur.execute("SELECT do.day,us.id,ab.kind FROM days_off as do JOIN users AS us ON us.id = do.userid JOIN absence_type AS ab ON ab.id = do.absenceId ").fetchall()
    db.close()
    for row in rows:
        data.append([row[0].strftime('%Y-%m-%d'), row[1], row[2]])

    return json.dumps(data)

@bp.route("/calendar/exceptions", methods=["POST"])
def addBusinessDayException():
    creation = dt.datetime.now()
    day = request.form.get("day")
    # month = request.form.get("month")
    # year = request.form.get("year")

    userId = 1
    absenceId = 1
    day = "{}".format(day)

    db = get_db()
    cur = db.cursor()
    cur.execute('INSERT INTO days_off(userid, absenceid, day) VALUES (?, ?, ?)', (userId, absenceId, day))
    db.commit()
    db.close()

    return { "msg": "Day {} added to day exceptions.".format(day) }, status.HTTP_201_CREATED

@bp.route("/calendar/exceptions", methods=["DELETE"])
def delBusinessDayException():
    creation = dt.datetime.now()
    day = request.form.get("day")
    # month = request.form.get("month")
    # year = request.form.get("year")
    day = "{}".format(day)

    db = get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM days_off WHERE day = ?', [day])
    db.commit()
    db.close()
    return { "msg": "Day {} removed from day exceptions.".format(day) }, status.HTTP_201_CREATED
