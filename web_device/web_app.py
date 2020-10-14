from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
import json
import platform
import setproctitle
import psutil
import configparser
import requests
import subprocess

app = Flask(__name__)

@app.route('/')
def bar_graph():
    return render_template('bar_graph.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/setting')
def setting():
    return render_template('setting.html')

#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/resource')
def get_resource():
    try:
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory()[2]  # physical memory usage
        hdd_percent = psutil.disk_usage('/')[3]

        resource_dict = {'cpu': cpu_percent, 'mem': mem_percent, 'hdd': hdd_percent}
        resource_json = json.dumps(resource_dict)

        return resource_json

    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_resource'}), 500

#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/process')
def get_process():
    try:
        result_status = dict()
        web_status  = "ninewatt_web" in (p.name() for p in psutil.process_iter())
        result_status["ninewatt_web"] = web_status 
        dict_rows_json = json.dumps(result_status)

        return dict_rows_json
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_process'}), 500

@app.route('/user_site_id/<site_id>')
def change_site_id(site_id):
    config=configparser.ConfigParser()
    config.read("config.ini")
    config['INFO']['site_id']=site_id

    with open('config.ini','w') as configfile:
        config.write(configfile)

    return jsonify(success=True)
#사이트 ID 받아서 config.ini 수정해줌


#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/user_site_id')
def user_site_id():
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        site_id = config.get("INFO", "SITE_ID")

        return jsonify({"site_id" : site_id}), 200
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_process'}), 500


#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/server_ip')
def server_ip():
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        server_ip = config.get("INFO", "SERVER_IP")
        return jsonify({"server_ip" : server_ip}), 200
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_process'}), 500

@app.route('/get/raw/<start_date>/<end_date>')
def get_raw(start_date,end_date):
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        site_id = config.get("INFO", "SITE_ID")
        server_ip = config.get("INFO", "SERVER_IP")

        # req_url = 'http://' + server_ip + ':5000/history/get/raw/' + site_id + '/' + start_date+'/'+end_date
        req_url = 'http://14.63.163.204:5000/history/get/raw/10000010/2007010100/2007012300'
        
        print(req_url)

        res = requests.get(req_url, timeout=5)
        #print(res.text)

        return jsonify(res.json()), 200
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_process'}), 500

#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/get/day/<date>')
def get_day(date):
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        site_id = config.get("INFO", "SITE_ID")
        server_ip = config.get("INFO", "SERVER_IP")

        # req_url = 'http://' + server_ip + ':5000/history/get/day/' + site_id + '/' + date
        req_url = 'http://14.63.163.204:5000/history/get/day/10000010/2007'
        
        print(req_url)

        res = requests.get(req_url, timeout=5)
        #print(res.text)

        return jsonify(res.json()), 200
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_process'}), 500


#author: hyeok0724.kim@ninewatt.com
#param: start_date, end_date
#ex) start_date -> 2008010100, end_date -> 2008012300
#description: Get history from raw_history
@app.route('/get/month/<date>')
def get_month(date):
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        site_id = config.get("INFO", "SITE_ID")
        server_ip = config.get("INFO", "SERVER_IP")

        #req_url = 'http://' + server_ip + ':5000/history/get/month/' + site_id + '/' + date
        req_url = 'http://14.63.163.204:5000/history/get/month/10000010/2007'

        print(req_url)
        
        res = requests.get(req_url, timeout=5)
        #print(res.text)

        return jsonify(res.json()), 200
    
    except Exception as e:
        #_LOGGER.error(e)
        print(e)
        return jsonify({'error': 'get_process'}), 500

@app.route('/xscreensaver/<status>')
def xscreensaver_control(status):
    if status == 'off':
        subprocess.call("xscreensaver-command -exit", shell=True)
        return jsonify({'success':"xscreensaver off"}), 200
    elif status == 'on':
        subprocess.call("xscreensaver -no-splash &", shell=True)
        return jsonify({'success':"xscreensaver on"}), 200
    else:
        print("error")
        return jsonify({'error':"xscreensaver error"}), 500

@app.route('/xscreensaver')
def xscreensaver_status():
    pid_check = "xscreensaver" in (p.name() for p in psutil.process_iter())

    if pid_check == True:
        return jsonify({'xscreensaver_status':"on"}), 200
    else:
        return jsonify({'xscreensaver_status':"off"}), 200


if __name__ == '__main__':
    if platform.system() == "Linux":
        setproctitle.setproctitle('ninewatt_web')

    app.run(host="0.0.0.0", port="7070", debug="True")