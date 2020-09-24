from flask import Flask, render_template, request, redirect
import psycopg2 as pg2
import db_api
import json
import calendar
import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
oDB_Api = db_api.cDB_Api()

@app.route('/')
def index():
    return "Hello"

#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/site/add/<device_id>')
def add_device(device_id):
    result = oDB_Api.add_site(device_id)
    dict_rows_json = json.dumps(result)
    return dict_rows_json

#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/site/del/<site_id>')
def del_device(site_id):
    result = oDB_Api.del_site(site_id)
    return result

#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/site/get/all')
def get_site_info():
    result = oDB_Api.get_site_all()
    dict_rows_json = json.dumps(result)
    return dict_rows_json


#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/history/add/<site_id>/<value>')
def add_raw_history(site_id, value):
    #Todo
    result = oDB_Api.add_raw_history(site_id, value)
    return result


#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/history/get/raw/<site_id>/<start_date>/<end_date>')
def get_raw_history(site_id, start_date, end_date):

    #Convert start_date, end_date to 2020-08-01 00:00:00
    length = 2
    tmp_txt = [start_date[i:i+length] for i in range(0, len(start_date), length)]
    str_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " " + tmp_txt[3] + ":" + tmp_txt[4] + ":00"

    tmp_txt = [end_date[i:i+length] for i in range(0, len(end_date), length)]
    end_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " " + tmp_txt[3] + ":" + tmp_txt[4] + ":00"

    raw_data = oDB_Api.get_raw_history(site_id, str_dt_txt, end_dt_txt)
    dict_rows_json = json.dumps(raw_data)

    return dict_rows_json

#author: hyeok0724.kim@ninewatt.com
#param: site_id, date
#ex) site_id -> 10000001, date -> 2008 (20.8)
#description: Get history from raw_history
@app.route('/history/get/day/<site_id>/<date>')
def get_day_history(site_id, date):
    length = 2
    tmp_txt = [date[i:i+length] for i in range(0, len(date), length)]

    str_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-01 00:00:00"
    tmp_year = int("20" + tmp_txt[0])
    last_day = str(calendar.monthrange(tmp_year, int(tmp_txt[1]))[1])
    
    end_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + last_day + " 00:00:00"    
    raw_data = oDB_Api.get_day_history(site_id, str_dt_txt, end_dt_txt)
    dict_rows_json = json.dumps(raw_data)
    return dict_rows_json

#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/history/get/month/<site_id>/<date>')
def get_month_history(site_id, date):
    length = 2
    tmp_txt = [date[i:i+length] for i in range(0, len(date), length)]
    end_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-01 00:00:00"
    end_date = datetime.datetime.strptime(end_dt_txt, '%Y-%m-%d %H:%M:%S')

    delta_time = relativedelta(months=12)

    str_dt_txt = str(end_date - delta_time)

    raw_data = oDB_Api.get_day_history(site_id, str_dt_txt, end_dt_txt)
    dict_rows_json = json.dumps(raw_data)
    
    return dict_rows_json
	
if __name__ == "__main__":
    app.run(debug=True)