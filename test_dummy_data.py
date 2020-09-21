#-*- coding:utf-8 -*-

import configparser
import datetime
import json
import psycopg2 as pg2

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
        self.cursor = self.db.cursor()

    # disconnect from server
    def db_disconn(self):
        self.cursor.close()
        self.db.close()

    #ex) start_date -> 200801
    def create_dummy(self, site_id, start_date):
        #self.db_conn()
        
        length = 2
        tmp_txt = [start_date[i:i+length] for i in range(0, len(start_date), length)]
        str_dt_txt = "20" + tmp_txt[0] + "-" + tmp_txt[1] + "-" + tmp_txt[2] + " 00:00:00"
        
        str_date = datetime.datetime.strptime(str_dt_txt, '%Y-%m-%d %H:%M:%S')

        delta_time = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=1, hours=0, weeks=0)

        next_date = str_date + delta_time

        print(next_date)

        """
        sql = 'INSERT INTO raw_history(site_id, date, value) VALUES (%s, %s, %s)'

        try: 
            self.cursor.execute(sql, (site_id, sql_date, value))
            print("Success")
            return "validate"

        except Exception as e:
            #self.log.logger.info("SQL: %s",e)
            print(e)
            return "error"
        
        finally:
            self.db_disconn()
        """

if __name__ == "__main__":
    oDB_Api = cDB_Api()
    #oDB_Api.add_site("999", "12:34:56:78:AB")
    #oDB_Api.insert_raw_history("123", "999")
    oDB_Api.create_dummy('123', '200801')
    