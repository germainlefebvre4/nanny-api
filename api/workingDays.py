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
import pandas


from api.db import get_db

bp = Blueprint("workingdays", __name__, url_prefix="/api")


# To delete in the future
@bp.route("/contracts/<int:contractId>/workingdays", methods=["GET"])
def getContractWorkingDays(contractId):
    userId = 1
    
    db = get_db()
    cur = db.cursor()
    rows = cur.execute("\
            SELECT \
                wd.id,wd.daytypeid,wd.day, \
                co.userid,co.nannyid,\
                dt.kind \
            FROM working_days as wd \
            JOIN contracts as co ON co.id = wd.contractid \
            JOIN day_type AS dt ON dt.id = wd.daytypeid \
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
                    wd.id,wd.daytypeid,wd.day,\
                    co.userid,\
                    dt.kind \
                FROM working_days as wd \
                JOIN contracts as co ON co.id = wd.contractid \
                JOIN day_type AS dt ON dt.id = wd.daytypeid \
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
        startDay = "{:04d}-{:02d}-{:02d}".format(year, month, 1)
        endDay = "{:04d}-{:02d}-{:02d}".format(year, month, 31)
        
        db = get_db()
        cur = db.cursor()
        rows = cur.execute("\
                SELECT \
                    wd.id,wd.daytypeid,wd.day,\
                    us.firstname,\
                    dt.kind, \
                    co.userid \
                FROM working_days as wd \
                JOIN contracts as co ON co.id = wd.contractid \
                JOIN users AS us ON us.id = co.userid \
                JOIN day_type AS dt ON dt.id = wd.daytypeid \
                WHERE wd.contractid = ? \
                    AND co.userid = ? \
                    AND dt.id < 50 \
                    AND wd.day >= ? \
                    AND wd.day <= ?", 
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
        weekmask_list = [int(x) for x in contract_info.get("weekdays").split(",")]

        business_days_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask="Mon Tue Wed Thu Fri", holidays=holidays_fra).format()
        business_days_inherited_pandas = pandas.bdate_range(start=startDay, end=endDay, freq="C", weekmask="Mon Tue Wed Thu Fri", holidays=holidays_fra+workingdays_list).format()
        # business_days_count = len(business_days_pandas)
        # business_days_inherited_count = len(business_days_inherited_pandas)
        print([x[0] for x in holidays.FRA(years=year).items() if datetime.strftime(x[0], "%m") == "{:02}".format(month)])

        # holidays_fra = [
        #     dict(daytypeid=0, kind="Jour férié", day=dt.datetime.strftime(x[0], "%Y-%m-%d")) 
        #     for x in holidays.FRA(years=year).items() 
        #     if dt.datetime.strftime(x[0], "%m") == "{:02}".format(month)
        # ]

        # print(holidays_fra)
        # print(business_days_pandas)
        # print(business_days_inherited_pandas)
        
        data =  [
            dict(
                day=x["day"],
                daytypeid=x["daytypeid"],
                kind=x["kind"]
            )
            for x in workingdays
        ] + [
            dict(
                day=x,
                daytypeid=51,
                kind="Jour férié"
            )
            for x in holidays_fra
        ] + [
            dict(
                day=x,
                daytypeid=50,
                kind="Hérité du contrat",
            )
            for x in business_days_inherited_pandas
        ]
        data.sort(key=lambda x: x["day"])
        
        return jsonify(data)

    # elif year and month and day:
    #     startDay = "{:04d}-{:02d}-{:02d}".format(year, month, day)

    #     db = get_db()
    #     cur = db.cursor()
    #     row = cur.execute("\
    #             SELECT \
    #                 wd.id,wd.daytypeid,wd.day,\
    #                 us.firstname,\
    #                 dt.kind, \
    #                 co.userid \
    #             FROM working_days as wd \
    #             JOIN contracts as co ON co.id = wd.contractid \
    #             JOIN users AS us ON us.id = co.userid \
    #             JOIN day_type AS dt ON dt.id = wd.daytypeid \
    #             WHERE wd.day = ?",
    #             [startDay]
    #         ).fetchone()
    #     db.close()

    #     data = []
    #     if not row:
    #         data = []
    #     else:
    #         data = [dict(row)]

    #     return jsonify(data)
    else:
        return jsonify(msg='Please select a year, month and day value.'), 422


@bp.route("/workingdays", methods=["POST"])
def addWorkingDays():
    creation_date = dt.datetime.now()
    day = request.get_json().get("day")
    day_type = request.get_json().get("day_type")

    if day and day_type:

        userId = 1
        daytypeid = "{}".format(day_type)
        day = "{}".format(day)

        db = get_db()
        cur = db.cursor()
        rows = cur.execute("\
                SELECT day, userId, daytypeid \
                FROM working_days as wd \
                JOIN contracts as co ON co.id = wd.contractid \
                JOIN users AS us ON us.id = co.userid \
                WHERE wd.day = ? \
                    AND co.userId = ? \
                    AND wd.daytypeid = ?",
                [day, userId, daytypeid]
            ).fetchall()
        if len(rows) > 0:
            db.close()
            current_app.logger.info("Day {} daytypeid {} already exists.".format(day, day_type))
            return { "msg": "Day {} daytypeid {} already exists.".format(day, day_type) }, status.HTTP_409_CONFLICT

        cur = db.cursor()
        cur.execute("\
                INSERT INTO working_days(userid, daytypeid, day, creation_date) \
                VALUES (?, ?, ?, ?)", 
                (userId, daytypeid, day, creation_date)
            )
        db.commit()
        db.close()

        return { "msg": "Day {} daytypeid {} added to day exceptions.".format(day, day_type) }, status.HTTP_201_CREATED
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