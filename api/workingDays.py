# coding: utf8

from flask import Blueprint
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask import current_app
from flask_cors import CORS
from flask_api import status
import json
import datetime as dt
import holidays
import sqlite3

from api.db import get_db

bp = Blueprint("workingdays", __name__, url_prefix="/api")


# To delete in the future
@bp.route("/workingdays", methods=["GET"])
def getWorkingDaysAll():
    db = get_db()
    cur = db.cursor()
    rows = cur.execute("SELECT do.id,do.userid,do.absenceid,do.day,us.firstname,ab.kind \
                        FROM working_days as do \
                        JOIN users AS us ON us.id = do.userid \
                        JOIN absence_type AS ab ON ab.id = do.absenceId"
        ).fetchall()
    db.close()

    data = []
    for row in rows:
        data.append(dict(row))

    return jsonify(data)

@bp.route("/workingdays/<int:workingdaysId>", methods=["GET"])
def getWorkingDaysById(workingdaysId):
    userId = 0
    
    try:
        db = get_db()
        cur = db.cursor()
        row = cur.execute("\
                SELECT do.id,do.userid,do.absenceid,do.day,us.firstname,ab.kind \
                FROM working_days as do \
                JOIN users AS us ON us.id = do.userid \
                JOIN absence_type AS ab ON ab.id = do.absenceId \
                WHERE do.id = ?", 
                [workingdaysId]
            ).fetchone()
        db.close()

        data = {}
        data = dict(row)

        return jsonify(data), status.HTTP_200_OK
    except:
        data = {"msg": "Entry does not exist."}
        return jsonify(data), status.HTTP_404_NOT_FOUND


@bp.route("/workingdays/search", methods=["GET"])
def getWorkingDaysByRangeDate():
    year = request.args.get('year', default=None, type=int)
    month = request.args.get('month', default=None, type=int)
    day = request.args.get('day', default=None, type=int)

    
    if year and month and not day:
        startDay = "{:04d}-{:02d}-{:02d}".format(year, month, 1)
        endDay = "{:04d}-{:02d}-{:02d}".format(year, month, 31)
        
        db = get_db()
        cur = db.cursor()
        rows = cur.execute("\
                SELECT do.id,do.userid,do.absenceid,do.day,us.firstname,ab.kind \
                FROM working_days as do \
                JOIN users AS us ON us.id = do.userid \
                JOIN absence_type AS ab ON ab.id = do.absenceId \
                WHERE do.day >= ? AND do.day <= ?", 
                [startDay, endDay]
            ).fetchall()
        db.close()

        workingdays = []
        for row in rows:
            workingdays.append(dict(row))

        holidays_fra = [dict(absenceid=0, kind="Jour férié", day=dt.datetime.strftime(x[0], "%Y-%m-%d")) for x in holidays.FRA(years=year).items() if dt.datetime.strftime(x[0], "%m") == "{:02}".format(month)]

        data = workingdays + holidays_fra

        return jsonify(data)

    elif year and month and day:
        startDay = "{:04d}-{:02d}-{:02d}".format(year, month, day)

        db = get_db()
        cur = db.cursor()
        row = cur.execute("\
                SELECT do.id,do.userid,do.absenceid,do.day,us.firstname,ab.kind \
                FROM working_days as do \
                JOIN users AS us ON us.id = do.userid \
                JOIN absence_type AS ab ON ab.id = do.absenceId \
                WHERE do.day = ?", 
                [startDay]
            ).fetchone()
        db.close()

        data = []
        if not row:
            data = []
        else:
            data = [dict(row)]

        return jsonify(data)
    else:
        return jsonify(msg='Please select a year, month and day value.'), 422


@bp.route("/workingdays", methods=["POST"])
def addWorkingDays():
    creation_date = dt.datetime.now()
    day = request.get_json().get("day")
    absence = request.get_json().get("absence")

    if day and absence:

        userId = 1
        absenceId = "{}".format(absence)
        day = "{}".format(day)

        db = get_db()
        cur = db.cursor()
        rows = cur.execute("\
                SELECT day, userId, absenceId FROM working_days \
                WHERE day = ? AND userId = ? and absenceId = ?", 
                [day, userId, absenceId]
            ).fetchall()
        if len(rows) > 0:
            db.close()
            current_app.logger.info("Day {} absenceId {} already exists.".format(day, absence))
            return { "msg": "Day {} absenceId {} already exists.".format(day, absence) }, status.HTTP_409_CONFLICT

        cur = db.cursor()
        cur.execute("\
                INSERT INTO working_days(userid, absenceid, day, creation_date) \
                VALUES (?, ?, ?, ?)", 
                (userId, absenceId, day, creation_date)
            )
        db.commit()

        db.close()

        return { "msg": "Day {} absenceId {} added to day exceptions.".format(day, absence) }, status.HTTP_201_CREATED
    else:
        return jsonify(msg='Please give data.'), 422

@bp.route("/workingdays/<int:workingdaysId>", methods=["DELETE"])
def delWorkingDays(workingdaysId):
    if workingdaysId:
        db = get_db()
        cur = db.cursor()
        cur.execute('DELETE FROM working_days WHERE id = ?', [workingdaysId])
        db.commit()
        db.close()
        return { "msg": "Day  {} removed from day exceptions.".format(workingdaysId) }, status.HTTP_200_OK
    else:
        return jsonify(msg='Please give data.'), 422