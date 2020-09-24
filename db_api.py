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
        #self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        

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
            
            sql = "SELECT site_id FROM site_info WHERE device = '" + device + "'"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data

        except Exception as e:
            #self.log.logger.info("SQL: %s",e)
            print(e)
            return "error"
        
        finally:
            self.db_disconn()

    def del_site(self, site_id):
        self.db_conn()

        try: 
            sql = "DELETE FROM site_info WHERE site_id = " + site_id
            self.cursor.execute(sql)
            
            return "success"

        except Exception as e:
            #self.log.logger.info("SQL: %s",e)
            print(e)
            return "error"
        
        finally:
            self.db_disconn()

    
    def add_raw_history(self, site_id, value):
        self.db_conn()

        now_date = datetime.datetime.now()
        sql_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO raw_history(site_id, date, value) VALUES (%s, %s, %s)'

        try: 
            self.cursor.execute(sql, (site_id, sql_date, value))
            return "success"

        except Exception as e:
            #self.log.logger.info("SQL: %s",e)
            print(e)
            return "error"
        
        finally:
            self.db_disconn()
        
    def get_site_all(self):
        self.db_conn()
        
        try: 
            sql = "SELECT site_id, device FROM site_info"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data

        except Exception as e:
            #self.log.logger.info("SQL: %s",e)
            print(e)
            return "error"
        
        finally:
            self.db_disconn()

    def get_day_history(self, site_id, start_date, end_date):
        self.db_conn()
        sql = "SELECT TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS') as date, value FROM day_history WHERE site_id = '" + site_id + "' AND date >='" + start_date + "' AND date <='" + end_date + "'"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        return data

    def get_month_history(self, site_id, start_date, end_date):
        self.db_conn()
        sql = "SELECT TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS') as date, value FROM month_history WHERE site_id = '" + site_id + "' AND date >='" + start_date + "' AND date <='" + end_date + "'"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        print(data)
        return data

    def get_raw_history(self, site_id, start_date, end_date):
        self.db_conn()
        #sql = "SELECT TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS') as date, TO_CHAR(value, '999') FROM raw_history WHERE site_id = '" + site_id + "' AND date >'" + start_date + "' AND date <'" + end_date + "'"
        sql = "SELECT TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS') as date, value FROM raw_history WHERE site_id = '" + site_id + "' AND date >'" + start_date + "' AND date <'" + end_date + "'"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        return data

##############=================================================================##########################
##############=================================================================##########################
##############=================================================================##########################

    def setDC_history(self, targetPower, present_power, predict_power):
        self.db_conn()
        now_date = datetime.datetime.now()
        sql_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO dc_history_tb(date_id, target_power, present_power, predict_power) VALUES (%s, %s, %s, %s)'
        try: 
            self.cursor.execute(sql, (sql_date, targetPower, present_power, predict_power))
            return "validate"

        except Exception as e:
            self.log.logger.info("SQL: %s",e)
            return "error"
        
        finally:
            self.db_disconn()


    # get data from database
    # ex) date -> 2019-12-10'
    def getDC_history(self, date):
        self.db_conn()
        startDate = date + ' 00:00:00'
        endDate = date + ' 23:59:59'
        #sql = "SELECT DATE_FORMAT(date_id, '%H:%i:%S') AS date_id, target_power, present_power, predict_power FROM dc_history_tb WHERE date_id >'" + startDate + "' AND date_id <'" + endDate + "'"
        sql = "SELECT DATE_FORMAT(date_id, '%H:%i:%S') AS date_id, target_power, present_power, predict_power FROM dc_history_tb WHERE date_id >'" + startDate + "' AND date_id <'" + endDate + "'"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        return data


    # get data from database
    def getDC_historyLastHistory(self):
        self.db_conn()
        sql = "SELECT * FROM dc_history_tb ORDER BY date_id DESC limit 1"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        return data
    
    # Insert agent_history
    def setAgentHistory(self, mode, target_power, active):
        self.db_conn()
        now_date = datetime.datetime.now()
        sql_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO agent_history_tb(date_id, mode, target_power, active) VALUES(" + "'" +  sql_date + "'" + "," + "'" + mode + "'," +  target_power + ",'" + active + "')"

        try:
            self.cursor.execute(sql)
            self.log.logger.info("SQL: %s",sql)
            self.db_disconn()
            return "validate"

        except Exception as e:
            self.log.logger.info("SQL: %s",e)
            self.db_disconn()
            return "error"

    def getLastAgentHistory(self):
        self.db_conn()
        sql = "SELECT * FROM agent_history_tb ORDER BY date_id DESC limit 1"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        return data

    # Insert control_history
    def setControlHistory(self, mode, target_power, active):
        self.db_conn()
        now_date = datetime.datetime.now()
        sql_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO control_history_tb(date_id, mode, target_power, active) VALUES(" + "'" +  sql_date + "'" + "," + "'" + mode + "'," +  target_power + ",'" + active + "')"

        try:
            self.cursor.execute(sql)
            self.log.logger.info("SQL: %s",sql)
            self.db_disconn()
            return "validate"

        except Exception as e:
            self.log.logger.info("SQL: %s",e)
            self.db_disconn()
            return "error"

    def getLastControlHistory(self):
        self.db_conn()
        sql = "SELECT * FROM control_history_tb ORDER BY date_id DESC limit 1"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        return data

# if __name__ == "__main__":
#     oDB_Api = cDB_Api()
#     #oDB_Api.add_site("999", "12:34:56:78:AB")
#     oDB_Api.insert_raw_history("123", "999")


