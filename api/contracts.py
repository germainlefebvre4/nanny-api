# coding: utf8

from flask import Blueprint
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask import current_app
from flask_cors import CORS
from flask_api import status
import json
from datetime import datetime
import holidays
import sqlite3

from api.db import get_db

bp = Blueprint("contracts", __name__, url_prefix="/api")


@bp.route("/contracts", methods=["GET"])
def getContractsAll():
    db = get_db()
    cur = db.cursor()
    rows = cur.execute("SELECT co.id,co.userid,co.nannyid \
            FROM contracts as co \
            JOIN users AS us ON us.id = co.userid \
            JOIN nannies AS na ON na.id = co.nannyid"
        ).fetchall()
    db.close()
    
    data = []
    for row in rows:
        data.append(dict(row))

    return jsonify(data)

@bp.route("/contracts/<int:contractId>", methods=["GET"])
def getContractsById(contractId):
    userId = 1
    
    try:
        db = get_db()
        cur = db.cursor()
        row = cur.execute("\
                SELECT co.id, co.userid as user_id, co.nannyid as nanny_id \
                FROM contracts as co \
                WHERE co.id = ? \
                    AND userid = ?",
                [contractId, userId]
            ).fetchone()
        db.close()

        data = {}
        data = dict(row)

        return jsonify(data), status.HTTP_200_OK
    except:
        data = {"msg": "Entry does not exist."}
        return jsonify(data), status.HTTP_404_NOT_FOUND


@bp.route("/contracts", methods=["POST"])
def addContracts():
    userId = 1
    
    userId = request.get_json().get("user_id")
    nannyId = request.get_json().get("nanny_id")
    weekdays_tmp = request.get_json().get("weekdays")
    creation_date = datetime.now()

    if not (userId and nannyId and weekdays_tmp and isinstance(userId, int) and isinstance(nannyId, int)):
        return jsonify(msg='Please give data.'), 422
    
    weekdays = ",".join(map(str, weekdays_tmp))

    db = get_db()
    cur = db.cursor()
    rows = cur.execute("\
            SELECT userId, nannyId \
            FROM contracts as co \
            WHERE co.userId = ? \
                AND co.nannyId = ?",
            [userId, nannyId]
        ).fetchall()
    if len(rows) > 0:
        db.close()
        current_app.logger.info("Contract already exists. User {userId} Nanny {nannyId}")
        return { "msg": "Contract already exists." }, status.HTTP_409_CONFLICT

    cur = db.cursor()
    cur.execute("\
            INSERT INTO contracts(userid, nannyid, weekdays, creation_date) \
            VALUES (?, ?, ?, ?)", 
            [userId, nannyId, weekdays, creation_date]
        )
    db.commit()

    row = cur.execute("\
            SELECT id, userId, nannyId \
            FROM contracts as co \
            WHERE co.userId = ? \
                AND co.nannyId = ?",
            [userId, nannyId]
        ).fetchone()
        
    contractId = dict(row).get("id")

    db.close()

    return { "msg": f"Contract '{contractId}' created.", "id": contractId }, status.HTTP_201_CREATED

@bp.route("/contracts/<int:contractId>", methods=["PUT"])
def updateContracts(contractId):
    userId = 1
    
    updated_date = datetime.now()
    weekdays_tmp = request.get_json().get("weekdays")
    start_date = datetime.strptime(request.get_json().get("start_date"), "%Y-%m-%d")
    end_date = datetime.strptime(request.get_json().get("end_date"), "%Y-%m-%d")

    if not (weekdays_tmp and start_date and end_date):
        return jsonify(msg='Please give data.'), 422
    
    weekdays = ",".join(map(str, weekdays_tmp))

    db = get_db()
    cur = db.cursor()
    row = cur.execute("\
            SELECT co.id, co.userid \
            FROM contracts as co \
            WHERE co.id = ? \
                AND co.userId = ?",
            [contractId, userId]
        ).fetchone()
    
    if not row:
        return { "msg": f"Contract '{contractId}' not found." }, status.HTTP_404_NOT_FOUND
        
    cur = db.cursor()
    print(weekdays)
    print(type(weekdays))
    cur.execute("\
            UPDATE contracts \
            SET \
                weekdays = ? ,\
                start_date = ? ,\
                end_date = ? ,\
                updated_date = ? \
            WHERE id = ? \
                AND userid = ?", 
            [weekdays, start_date, end_date, updated_date, contractId, userId]
        )
    db.commit()
    db.close()

    return { "msg": f"Contract '{contractId}' created." }, status.HTTP_200_OK


@bp.route("/contracts/<int:contractId>", methods=["DELETE"])
def deleteContracts(contractId):
    userId = 1
    
    if contractId:
        db = get_db()
        cur = db.cursor()
        cur.execute("\
                DELETE FROM contracts \
                WHERE id = ? \
                    AND userId = ?", 
                [contractId, userId])
        db.commit()
        db.close()
        return { "msg": f"Contract '{contractId}' deleted." }, status.HTTP_200_OK
    else:
        return jsonify(msg='Please give data.'), 422