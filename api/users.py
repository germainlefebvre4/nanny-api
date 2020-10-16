# coding: utf8

from flask import Blueprint
from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask import current_app
from flask_cors import CORS
from flask_api import status
import json
import datetime as dt
import sqlite3

from api.db import get_db

bp = Blueprint("users", __name__, url_prefix="/api")

# To delete in the future
@bp.route("/users/profile", methods=["GET"])
def getUserProfile():
    userId = 1

    db = get_db()
    cur = db.cursor()
    row = cur.execute("\
            SELECT us.id, us.firstname, us.email \
            FROM users AS us \
            WHERE us.id = ?",
            [userId]
        ).fetchone()

    data =  dict(row)
    
    db.close()
    return jsonify(data), status.HTTP_200_OK

@bp.route("/users/contracts", methods=["GET"])
def getUserContracts():
    userId = 1

    db = get_db()
    cur = db.cursor()
    rows = cur.execute("\
            SELECT \
                co.id, co.userid, co.nannyid, co.start_date, co.end_date, \
                na.firstname \
            FROM contracts AS co \
            JOIN nannies as na ON na.id = co.nannyid \
            WHERE co.userid = ? \
            ORDER BY co.start_date DESC",
            [userId]
        ).fetchall()
    
    data = [dict(x) for x in rows]
    
    db.close()
    return jsonify(data), status.HTTP_200_OK

@bp.route("/users/contracts/orphans", methods=["GET"])
def getUserContractsOrphans():
    userId = 1

    db = get_db()
    cur = db.cursor()
    rows = cur.execute("\
            SELECT \
                co.id, co.userid, co.nannyid, co.start_date, co.end_date, \
                na.firstname \
            FROM contracts AS co \
            JOIN nannies as na ON na.id = co.nannyid \
            WHERE co.userid = ? \
                AND co.start_date IS ?",
            [userId, None]
        ).fetchall()
    
    data = [dict(x) for x in rows]
    
    db.close()
    return jsonify(data), status.HTTP_200_OK
