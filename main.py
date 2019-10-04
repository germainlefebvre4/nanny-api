from flask import Flask  # pip install flask
import sys
import datetime as dt
import datedelta as dd
import numpy as np

app = Flask(__name__)

salary_month_net = 367
fees_day_net = 3.08

@app.route("/business/month/<int:year>/<int:month>")
def getBusinessDays(year, month):
   start = dt.date( year, month, 1 )
   end = dt.date(year, month, 1) + dd.datedelta(months=1)
   bdays = int(np.busday_count( start, end , weekmask=[1,1,0,1,1,0,0] ))
   month_str = dt.date(year, month, 1).strftime("%B")
   fees_month_net = fees_day_net*bdays
   return  {"businessDays": { month_str: bdays, "salary": salary_month_net, "fees": fees_month_net }}
   return {}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
