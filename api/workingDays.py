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
import numpy
from datetime import datetime, date
from datedelta import datedelta
import calendar
import pandas


from api.db import get_db

bp = Blueprint("workingdays", __name__, url_prefix="/api")


WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# To delete in the future
@bp.route("/contracts/<int:contractId>/workingdays", methods=["GET"])
def getContractWorkingDays(contractId):
    userId = 1
    
    db = get_db()
    cur = db.cursor()
    rows = cur.execute("\
            SELECT \
                wd.id, wd.daytypeid as daytype_id, wd.day, \
                co.userid, co.nannyid,\
                dt.kind \
            FROM working_days as wd \
            JOIN contracts as co ON co.id = wd.contractid \
            JOIN day_types AS dt ON dt.id = wd.daytypeid \
            WHERE wd.contractid = ? \
                AND co.userid = ?",
            [contractId, userId]
        ).fetchall()
    db.close()

    data = []
    for row in rows:
        data.append(dict(row))

    return jsonify(data)


@bp.route("/contracts/<int:contractId>/workingdays/<int:workingdaysId>", methods=["GET"])
def getContractWorkingDaysById(contractId, workingdaysId):
    userId = 1
    
    try:
        db = get_db()
        cur = db.cursor()
        row = cur.execute("\
                SELECT \
                    wd.id, wd.daytypeid as daytype_id, wd.day,\
                    co.userid,\
                    dt.kind \
                FROM working_days as wd \
                JOIN contracts as co ON co.id = wd.contractid \
                JOIN day_types AS dt ON dt.id = wd.daytypeid \
                WHERE wd.contractid = ? \
                    AND co.userid = ? \
                    AND wd.id = ?",
                [contractId, userId, workingdaysId]
            ).fetchone()
        db.close()

        data = {}
        data = dict(row)

        return jsonify(data), status.HTTP_200_OK
    except:
        data = {"msg": "Entry does not exist."}
        return jsonify(data), status.HTTP_404_NOT_FOUND


@bp.route("/contracts/<int:contractId>/workingdays/search", methods=["GET"])
def getContractWorkingDaysByRangeDate(contractId):
    userId = 1
    
    year = request.args.get('year', default=None, type=int)
    month = request.args.get('month', default=None, type=int)
    day = request.args.get('day', default=None, type=int)
    
    db = get_db()
    cur = db.cursor()
    row = cur.execute("\
            SELECT co.id,co.weeks,co.weekdays,co.hours \
            FROM contracts as co \
            WHERE co.id = ? \
                AND co.userid = ?",
            [contractId, userId]
        ).fetchone()
    contract_info = dict(row)
    # db.close()
    # del(db)
    
    if year and month and not day:
        if int(year) < 1970 or int(month) < 1 or int(month) > 12:
            return jsonify(msg='Please select a year, month and day value.'), 422
        # Year and month
        lastDayOfTheMonth = calendar.monthrange(year, month)[1]
        startDay = "{:04d}-{:02d}-{:02d}".format(year, month, 1)
        endDay = "{:04d}-{:02d}-{:02d}".format(year, month, lastDayOfTheMonth)
        
        db = get_db()
        cur = db.cursor()
        rows = cur.execute("\
                SELECT \
                    wd.id, wd.daytypeid as daytype_id, wd.day,\
                    us.firstname,\
                    dt.kind,\
                    co.userid\
                FROM working_days as wd \
                JOIN contracts as co ON co.id = wd.contractid \
                JOIN users AS us ON us.id = co.userid \
                JOIN day_types AS dt ON dt.id = wd.daytypeid \
                WHERE wd.contractid = ? \
                    AND co.userid = ? \
                    AND wd.day >= ? \
                    AND wd.day <= ? \
                    AND dt.id < 50",
                [contractId, userId, startDay, endDay]
            ).fetchall()
        db.close()
        
        workingdays = []
        for row in rows:
            workingdays.append(dict(row))
        
        holidays_fra = [datetime.strftime(x[0], "%Y-%m-%d") 
            for x in holidays.FRA(years=year).items() 
            if datetime.strftime(x[0], "%m") == "{:02}".format(month)
        ]
        
        workingdays_list = [x["day"] for x in workingdays]
        weekmask_user = [bool(x) for x in contract_info.get("weekdays").split(",")]
        weekmask_list = [a and b for a, b in zip(weekmask_user, WEEKDAYS)]

        # business_days_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask="Mon Tue Wed Thu Fri", holidays=holidays_fra).format()
        business_days_inherited_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask="Mon Tue Wed Thu Fri", holidays=holidays_fra+workingdays_list)
        business_days_inherited_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask="Mon Tue Wed Thu Fri", holidays=holidays_fra+workingdays_list).format()
        
        data =  [
            dict(
                day=x["day"],
                daytype_id=x["daytype_id"],
                kind=x["kind"]
            )
            for x in workingdays
        ] + [
            dict(
                day=x,
                daytype_id=51,
                kind="Jour férié"
            )
            for x in holidays_fra
        ] + [
            dict(
                day=x,
                daytype_id=50,
                kind="Hérité du contrat",
            )
            for x in business_days_inherited_pandas
        ]
        data.sort(key=lambda x: x["day"])
        
        return jsonify(data)

    elif year and month and day:
        if int(year) < 1970 or int(month) < 1 or int(month) > 12 or int(day) < 1 or int(day) > calendar.monthrange(year, month)[1]:
            return jsonify(msg='Please select a year, month and day value.'), 422

        # Year, month and day
        lastDayOfTheMonth = calendar.monthrange(year, month)[1]
        startDay = "{:04d}-{:02d}-{:02d}".format(year, month, day)
        endDay = "{:04d}-{:02d}-{:02d}".format(year, month, day)

        db = get_db()
        cur = db.cursor()
        row = cur.execute("\
                SELECT \
                    wd.id, wd.daytypeid as daytype_id, wd.day,\
                    us.firstname,\
                    dt.kind, \
                    co.userid as user_id \
                FROM working_days as wd \
                JOIN contracts as co ON co.id = wd.contractid \
                JOIN users AS us ON us.id = co.userid \
                JOIN day_types AS dt ON dt.id = wd.daytypeid \
                WHERE wd.contractid = ? \
                    AND co.userid = ? \
                    AND wd.day >= ? \
                    AND wd.day <= ? \
                    AND dt.id < 50",
                [contractId, userId, startDay, endDay]
            ).fetchone()
        db.close()

        workingdays = []
        if row:
            workingdays.append(dict(row))
        
        holidays_fra = [datetime.strftime(x[0], "%Y-%m-%d")
            for x in holidays.FRA(years=year).items() 
            if datetime.strftime(x[0], "%m-%d") == "{:02}-{:02}".format(month, day)
        ]

        workingdays_list = [x["day"] for x in workingdays]
        weekmask_user = [bool(x) for x in contract_info.get("weekdays").split(",")]
        weekmask_list = [a and b for a, b in zip(weekmask_user, WEEKDAYS)]

        # business_days_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask="Mon Tue Wed Thu Fri", holidays=holidays_fra).format()
        business_days_inherited_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask="Mon Tue Wed Thu Fri", holidays=holidays_fra+workingdays_list).format()
        
        data =  [
            dict(
                id=x["id"],
                day=x["day"],
                daytype_id=x["daytype_id"],
                kind=x["kind"]
            )
            for x in workingdays
        ] + [
            dict(
                day=x,
                daytype_id=51,
                kind="Jour férié"
            )
            for x in holidays_fra
        ] + [
            dict(
                day=x,
                daytype_id=50,
                kind="Hérité du contrat",
            )
            for x in business_days_inherited_pandas
        ]
        data.sort(key=lambda x: x["day"])
        
        return jsonify(data)
    else:
        return jsonify(msg='Please select a year, month and day value.'), 422


@bp.route("/contracts/<int:contractId>/workingdays", methods=["POST"])
def addContractWorkingDays(contractId):
    userId = 1

    creation_date = dt.datetime.now()
    day = request.get_json().get("day")
    dayTypeId = request.get_json().get("daytype_id")

    if day and dayTypeId:

        db = get_db()
        cur = db.cursor()
        rows = cur.execute("\
                SELECT \
                    wd.day, wd.daytypeid as daytype_id, \
                    co.userId \
                FROM working_days as wd \
                JOIN contracts as co ON co.id = wd.contractid \
                WHERE wd.day = ? \
                    AND co.userId = ? \
                    AND wd.daytypeid = ?",
                [day, userId, dayTypeId]
            ).fetchall()
        if len(rows) > 0:
            db.close()
            current_app.logger.info("Day {} daytypeid {} already exists.".format(day, dayTypeId))
            return { "msg": "Day {} daytypeid {} already exists.".format(day, dayTypeId) }, status.HTTP_409_CONFLICT

        cur = db.cursor()
        cur.execute("\
                INSERT INTO working_days(contractid, daytypeid, day, creation_date) \
                VALUES (?, ?, ?, ?)", 
                (contractId, dayTypeId, day, creation_date)
            )
        db.commit()
        db.close()

        return { "msg": "Day {} daytypeid {} added to day exceptions.".format(day, dayTypeId) }, status.HTTP_201_CREATED
    else:
        return jsonify(msg='Please give data.'), 422

@bp.route("/contracts/<int:contractId>/workingdays/<int:workingdaysId>", methods=["DELETE"])
def delWorkingDays(contractId, workingdaysId):
    print(contractId, workingdaysId)
    if contractId and workingdaysId:
        db = get_db()
        cur = db.cursor()
        cur.execute("\
            DELETE FROM working_days \
            WHERE id = ?",
            [workingdaysId])
        db.commit()
        db.close()
        return { "msg": "Day  {} removed from day exceptions.".format(workingdaysId) }, status.HTTP_200_OK
    else:
        return jsonify(msg='Please give data.'), 422