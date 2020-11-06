#-*- coding:utf-8 -*-

import configparser
import datetime
import json
import psycopg2 as pg2
from psycopg2 import extras
from dateutil.relativedelta import relativedelta

class cDB_Api:
    def __init__(self):
        # Read Config file
        config = configparser.ConfigParser()
        config.read("config.ini")
        
        self.IP = config.get("DB_INFO", "IP")
        self.PORT = int(config.get("DB_INFO", "PORT"))
        self.USER = config.get("DB_INFO", "USER")
        self.PASSWD = config.get("DB_INFO", "PASSWD")
        self.DB = config.get("DB_INFO", "DB")
    
    # prepare a cursor object using cursor() method
    # Open database connection
    def db_conn(self):
        self.db = pg2.connect(host=self.IP, port=self.PORT, user=self.USER, password=self.PASSWD, database=self.DB)
        self.db.autocommit = True
        #self.cursor = self.db.cursor()
        self.cursor = self.db.cursor(cursor_factory=pg2.extras.DictCursor)

    # disconnect from server
    def db_disconn(self):
        self.cursor.close()
        self.db.close()
    
    # disconnect from server
    def db_disconn(self):
        self.cursor.close()
        self.db.close()

    def add_site(self, device):
        self.db_conn()
        now_date = datetime.datetime.now()
        sql_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO site_info(date, device) VALUES (%s, %s)'

        try: 
            self.cursor.execute(sql, (sql_date, device))
            return "validate"

        except Exception as e:
            #self.log.logger.info("SQL: %s",e)
            print(e)
            return "error"
        
        finally:
            self.db_disconn()

    #ex) start_date -> 200801
    def create_raw_history_dummy(self, site_id, start_date):
        self.db_conn()

        value = 10
        delta_time = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=1, hours=0, weeks=0)
        sql = 'INSERT INTO raw_history(site_id, date, value) VALUES (%s, %s, %s)'

        length = 2
        tmp_txt = [start_date[i:i+length] for i in range(0, len(start_date), length)]
        str_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " 00:00:00"
        
        str_date = datetime.datetime.strptime(str_dt_txt, '%Y-%m-%d %H:%M:%S')

        for i in range(1440):
            
            if i == 0:
                pass
            else:
                str_date = str_date + delta_time
                value = value + 1

            sql_date = str_date

            try: 
                self.cursor.execute(sql, (site_id, sql_date, value))
                print("Success %s" %sql_date)
            
            except Exception as e:
                #self.log.logger.info("SQL: %s",e)
                print(e)
                return "error"
        self.db_disconn()

    
    #ex) start_date -> 200801
    def create_day_history_dummy(self, site_id, start_date):
        self.db_conn()

        value = 10
        delta_time = datetime.timedelta(days=1, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
        sql = 'INSERT INTO day_history(site_id, date, value) VALUES (%s, %s, %s)'

        length = 2
        tmp_txt = [start_date[i:i+length] for i in range(0, len(start_date), length)]
        str_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " 00:00:00"
        
        str_date = datetime.datetime.strptime(str_dt_txt, '%Y-%m-%d %H:%M:%S')

        for i in range(19):
            
            if i == 0:
                pass
            else:
                str_date = str_date + delta_time
                value = value + 5

            sql_date = str_date

            try: 
                self.cursor.execute(sql, (site_id, sql_date, value))
                print("Success %s" %sql_date)
            
            except Exception as e:
                #self.log.logger.info("SQL: %s",e)
                print(e)
                return "error"
        self.db_disconn()

    
    #ex) start_date -> 200801
    def create_month_history_dummy(self, site_id, start_date):
        self.db_conn()

        value = 10
        delta_time = relativedelta(months=1)
        sql = 'INSERT INTO month_history(site_id, date, value) VALUES (%s, %s, %s)'

        length = 2
        tmp_txt = [start_date[i:i+length] for i in range(0, len(start_date), length)]
        str_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " 00:00:00"
        
        str_date = datetime.datetime.strptime(str_dt_txt, '%Y-%m-%d %H:%M:%S')

        for i in range(13):
            
            if i == 0:
                pass
            else:
                str_date = str_date + delta_time
                value = value + 10

            sql_date = str_date

            try: 
                self.cursor.execute(sql, (site_id, sql_date, value))
                print("Success %s" %sql_date)
            
            except Exception as e:
                #self.log.logger.info("SQL: %s",e)
                print(e)
                return "error"
        self.db_disconn()

    def get_day_history(self, site_id, start_date, end_date):
        self.db_conn()
        sql = "SELECT TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS') as date, value FROM day_history WHERE site_id = '" + site_id + "' AND date >='" + start_date + "' AND date <='" + end_date + "'"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        print(type(data))

        for row in data:
            print(type(row))
            print(row)
            print(row['value'])

        #dict_rows = {"modbus_info" : data['value']}

        self.db_disconn()

        #dict_rows_json = json.dumps(dict_rows)
        
        #print(dict_rows_json)
        #return dict_rows_json
        return "hello"

if __name__ == "__main__":
    oDB_Api = cDB_Api()
    #oDB_Api.add_site("12:34:56:78:AB")
    #oDB_Api.create_raw_history_dummy('10000010', '200701')
    #oDB_Api.create_day_history_dummy('10000010', '200801')
    #oDB_Api.create_month_history_dummy('10000010', '190801')
    #oDB_Api.get_day_history('10000013', '2020-09-01 00:00:00', '2020-09-20 00:00:00')
    #oDB_Api.create_month_history_dummy('10000013', '190901')
    oDB_Api.create_month_history_dummy('10000056', '191001')
    oDB_Api.create_day_history_dummy('10000056', '201001')
    