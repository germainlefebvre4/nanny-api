# coding: utf8

from flask import Blueprint
from flask import Flask, redirect, url_for, request, render_template  # pip install flask
from flask import current_app
from flask_cors import CORS
from flask_api import status
import json
import datetime as dt
import sqlite3

from api.db import get_db

bp = Blueprint("calendar", __name__)

@bp.route("/calendar/exceptions", methods=["GET"])
@bp.route("/calendar/exceptions/<int:year>/<int:month>", methods=["GET"])
def getBusinessDayException(year, month):
    startDay = "{:04d}-{:02d}-{:02d}".format(year, month, 1)
    endDay = "{:04d}-{:02d}-{:02d}".format(year, month, 31)
    data = []

    db = get_db()
    cur = db.cursor()
    rows = cur.execute("SELECT do.day,us.firstname,ab.kind FROM days_off as do JOIN users AS us ON us.id = do.userid JOIN absence_type AS ab ON ab.id = do.absenceId WHERE do.day >= ? AND do.day <= ?", [startDay, endDay]).fetchall()
    # rows = cur.execute("SELECT do.day,us.firstname,ab.kind FROM days_off as do JOIN users AS us ON us.id = do.userid JOIN absence_type AS ab ON ab.id = do.absenceId ").fetchall()
    db.close()
    for row in rows:
        data.append([row[0], row[1], row[2]])

    return json.dumps(data)

@bp.route("/calendar/exceptions", methods=["POST"])
def addBusinessDayException():
    creation = dt.datetime.now()
    day = request.form.get("day")
    absence = request.form.get("absence")

    userId = 1
    absenceId = "{}".format(absence)
    day = "{}".format(day)

    db = get_db()
    cur = db.cursor()
    rows = cur.execute("SELECT day, userId, absenceId FROM days_off WHERE day = ? AND userId = ? and absenceId = ?", [day, userId, absenceId]).fetchall()
    if len(rows) > 0:
        db.close()
        current_app.logger.info("Day {} absenceId {} already exists.".format(day, absence))
        return { "msg": "Day {} absenceId {} already exists.".format(day, absence) }, status.HTTP_409_CONFLICT

    cur = db.cursor()
    cur.execute('INSERT INTO days_off(userid, absenceid, day) VALUES (?, ?, ?)', (userId, absenceId, day))
    db.commit()

    db.close()

    return { "msg": "Day {} absenceId {} added to day exceptions.".format(day, absence) }, status.HTTP_201_CREATED

@bp.route("/calendar/exceptions", methods=["DELETE"])
def delBusinessDayException():
    creation = dt.datetime.now()
    absence = request.form.get("absence")
    absenceId = "{}".format(absence)
    day = request.form.get("day")
    day = "{}".format(day)

    current_app.logger.info("absenceId="+absenceId)
    current_app.logger.info("day="+day)

    db = get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM days_off WHERE absenceid = ? and day = ?', [absenceId, day])
    db.commit()
    db.close()
    return { "msg": "Day {} absenceId {} removed from day exceptions.".format(day, absence) }, status.HTTP_201_CREATED

@bp.route("/select", methods=["GET"])
def getSelect():
    db = get_db()
    cur = db.cursor()
    cur.execute("select * from days_off")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append([x for x in row])
    return { "msg": data }
