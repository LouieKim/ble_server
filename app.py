from flask import Flask, render_template, request, redirect
import psycopg2 as pg2
import db_api

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"

@app.route('/site/add/<device_id>')
def add_device(device_id):
    return "Hello"

def db_connect():
    conn=pg2.connect(database="ble_db",user="postgres",password="postgres",host="52.79.241.100",port="5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM site_info")
    raw = cur.fetchall()
    for aa in raw:
        print(aa)
    
    conn.close()
	
if __name__ == "__main__":
    #db_connect()
    app.run(debug=True)