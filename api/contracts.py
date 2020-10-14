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


# To delete in the future
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
                WHERE co.id = ?",
                [contractId]
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
    creation_date = datetime.now()

    if not (userId or nannyId) or not (isinstance(userId, int) or isinstance(nannyId, int)):
        return jsonify(msg='Please give data.'), 422

    # nannyId = "{}".format(nannyId)
    # userId = "{}".format(userId)

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
            INSERT INTO contracts(userid, nannyid, creation_date) \
            VALUES (?, ?, ?)", 
            (userId, nannyId, creation_date)
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

@bp.route("/contracts/<int:contractId>", methods=["DELETE"])
def deleteContracts(contractId):
    if contractId:
        db = get_db()
        cur = db.cursor()
        cur.execute('DELETE FROM contracts WHERE id = ?', [contractId])
        db.commit()
        db.close()
        return { "msg": f"Contract '{contractId}' deleted." }, status.HTTP_200_OK
    else:
        return jsonify(msg='Please give data.'), 422