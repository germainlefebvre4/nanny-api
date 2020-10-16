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

bp = Blueprint("dayTypes", __name__, url_prefix="/api")

# To delete in the future
@bp.route("/daytypes", methods=["GET"])
def getDaysOffAll():
    data = []

    db = get_db()
    cur = db.cursor()
    rows = cur.execute("\
            SELECT dt.id as id, dt.kind as name \
            FROM day_types AS dt \
            WHERE id < 50"
        ).fetchall()
    db.close()

    for row in rows:
        data.append(dict(row))

    return jsonify(data)
