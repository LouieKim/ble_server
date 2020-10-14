import requests
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import platform

def calc_history():
    res = requests.get('http://localhost:5000/history/calc', timeout=10)
    print(res.text)

def create_history():
    res = requests.get('http://localhost:5000/history/create', timeout=10)
    print(res.text)

if __name__ == "__main__":

    sched = BackgroundScheduler()

    sched.add_job(create_history, 'cron', hour='0', id="create_history_id")
    sched.add_job(calc_history, 'cron', minute='*/5', id="calc_history_id")

    #sched.add_job(calc_req, 'cron', minute='*/2', id="calc_cron")
    #sched.add_job(polling_req, 'cron', minute='*/1', id="polling_cron")
    
    sched.start()

    while True:
        time.sleep(30)
        #print("Operating")
