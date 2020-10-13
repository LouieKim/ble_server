from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS,cross_origin
import psycopg2 as pg2
import db_api
import json
import calendar
import datetime
from dateutil.relativedelta import relativedelta
import psutil
import platform
#import setproctitle

app = Flask(__name__)
CORS(app, support_credentials=True)

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

    if result == "error":
        return jsonify({'error': 'Already registered'}), 500

    else:
        return jsonify({"site_id" : result[0][0]}), 200
   

#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/site/del/<site_id>')
def del_device(site_id):
    result = oDB_Api.del_site(site_id)

    if result == "error":
        return jsonify({'error': 'Wrong site_id'}), 500
    
    else:
        return jsonify({"success" : result}), 200


#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/site/get/all')
def get_site_info():
    result = oDB_Api.get_site_all()
    return jsonify({'site_ids': result}), 200


#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/site/get/<device_id>')
def get_site_id(device_id):
    result = oDB_Api.get_site_id(device_id)

    if result == "error":
        return jsonify({'error': "Wrong device_id"}), 500
    else:
        return jsonify({'site_id': result}), 200


#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/history/add/<site_id>/<value>')
def add_raw_history(site_id, value):
    #Todo
    result = oDB_Api.add_raw_history(site_id, value)

    if result == "error":
        return jsonify({'error': 'Wrong site_id'}), 500

    else:
        return jsonify({'success': result}), 200


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

    return jsonify({'raw_history': raw_data}), 200

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

    return jsonify({'day_history': raw_data}), 200

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

    delta_time = relativedelta(months=13)

    str_dt_txt = str(end_date - delta_time)

    raw_data = oDB_Api.get_month_history(site_id, str_dt_txt, end_dt_txt)
    
    return jsonify({'month_history': raw_data}), 200



#author: hyeok0724.kim@ninewatt.com
#param: 
#description: 
@app.route('/history/calc')
def calc_day_month():
    result = oDB_Api.calc_history()
    return jsonify({'calc_history': result}), 200


#author: hyeok0724.kim@ninewatt.com
#param: 
#description: 
@app.route('/history/create')
def create_day_month():
    result = oDB_Api.create_day_month_history()
    return jsonify({'calc_history': result}), 200

#author: hyeok0724.kim@ninewatt.com
#param:
#description: 
@app.route('/timenow')
def get_timenow():
    try:
        time_dict = dict()
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M')
        time_dict["time"] = nowDatetime[2:]
        dict_rows_json = json.dumps(time_dict)

        return dict_rows_json

    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_timenow'}), 500

	
if __name__ == "__main__":
    #if platform.system() == "Linux":
    #    setproctitle.setproctitle('ninewatt_app')

    app.run(host="0.0.0.0", port="5000", debug=True)