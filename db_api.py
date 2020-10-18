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
        #self.cursor = self.db.cursor(cursor_factory=pg2.extras.DictCursor)
        
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
            
            return site_id

        except Exception as e:
            #self.log.logger.info("SQL: %s",e)
            print(e)
            return "error"
        
        finally:
            self.db_disconn()

    def get_site_id(self, device):
        self.db_conn()
        
        try: 
            sql = "SELECT site_id, device FROM site_info WHERE device = '" + device + "'"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data

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

    
    def add_raw_history(self, site_id, value):
        self.db_conn()

        now_date = datetime.datetime.now()
        sql_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO raw_history(site_id, date, value) VALUES (%s, %s, %s)'

        try: 
            self.cursor.execute(sql, (site_id, sql_date, value))
            return value

        except Exception as e:
            #self.log.logger.info("SQL: %s",e)
            print(e)
            return "error"
        
        finally:
            self.db_disconn()
        
    

    def get_day_history(self, site_id, start_date, end_date):
        self.db_conn()
        sql = "SELECT TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS') as date, value FROM day_history WHERE site_id = '" + site_id + "' AND date >='" + start_date + "' AND date <='" + end_date + "'ORDER BY date ASC"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        return data

    def get_month_history(self, site_id, start_date, end_date):
        self.db_conn()
        sql = "SELECT TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS') as date, value FROM month_history WHERE site_id = '" + site_id + "' AND date >='" + start_date + "' AND date <='" + end_date + "'ORDER BY date ASC"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        return data

    def get_raw_history(self, site_id, start_date, end_date):
        self.db_conn()
        sql = "SELECT TO_CHAR(date, 'YYYY-MM-DD HH24:MI:SS') as date, value FROM raw_history WHERE site_id = '" + site_id + "' AND date >'" + start_date + "' AND date <'" + end_date + "'ORDER BY date DESC"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.db_disconn()
        return data

    #!!!! Todo asynchronous 해야함 꼭 잊지않기를 바람
    def calc_history(self):
        site_ids = self.get_site_all()

        now_dt_txt = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
        first_dt_txt = datetime.datetime.now().strftime('%Y-%m-01 00:00:00')

        for id in site_ids:
            day_history_validate = self.calc_day_history(id[0], now_dt_txt)
            month_history_validate = self.calc_month_history(id[0], first_dt_txt, now_dt_txt)
        
        return "success" if(day_history_validate == "success")&(month_history_validate == "success") else "fail"

    def calc_day_history(self, site_id, now_date):
        self.db_conn()
        sel_sql = "SELECT MAX(value) as mx_vlu, MIN(value) as min_vlu FROM raw_history WHERE site_id =" + str(site_id) + " AND date >= '" + now_date + "'"
        self.cursor.execute(sel_sql)
        data = self.cursor.fetchone()

        if (data[0] != None) & (data[1] != None):
            calc_result = data[0] - data[1]
            update_sql = "UPDATE day_history SET value = %s WHERE site_id = %s AND date = %s"
            self.cursor.execute(update_sql, (calc_result, site_id, now_date))        
            self.db_disconn()
            return "success"
        
        else:
            self.db_disconn()
            return "fail"
    
    def calc_month_history(self, site_id, first_date, now_date):
        self.db_conn()
        sel_sql = "SELECT SUM(value) FROM day_history WHERE site_id = %s AND date >= %s AND date <= %s"
        self.cursor.execute(sel_sql, (site_id, first_date, now_date))
        data = self.cursor.fetchone()

        if data != None:
            update_sql = "UPDATE month_history SET value = %s WHERE site_id = %s AND date = %s"
            self.cursor.execute(update_sql, (data, site_id, first_date))        
            self.db_disconn()
            return "success"
        
        else:
            self.db_disconn()
            return "fail"

    def create_day_month_history(self):
        site_ids = self.get_site_all()

        self.db_conn()     

        now_dt_txt = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
        first_dt_txt = datetime.datetime.now().strftime('%Y-%m-01 00:00:00')

        for site_id in site_ids:

            check_day_sql = "SELECT * FROM day_history WHERE site_id = %s AND date = %s"
            self.cursor.execute(check_day_sql, (site_id[0], now_dt_txt))
            data = self.cursor.fetchone()

            if data == None:
                day_insert_sql = "INSERT INTO day_history VALUES (%s, %s, %s)"
                self.cursor.execute(day_insert_sql, (site_id[0], now_dt_txt, 0))


            check_month_sql = "SELECT * FROM month_history WHERE site_id = %s AND date = %s"
            self.cursor.execute(check_month_sql, (site_id[0], first_dt_txt))
            data = self.cursor.fetchone()

            if data == None:
                month_insert_sql = "INSERT INTO month_history VALUES (%s, %s, %s)"
                self.cursor.execute(month_insert_sql, (site_id[0], first_dt_txt, 0))
        
        self.db_disconn()

        return "success"

        
# if __name__ == "__main__":
#     oDB_Api = cDB_Api()
#     #oDB_Api.add_site("999", "12:34:56:78:AB")
#     #oDB_Api.create_day_month_history()
#     oDB_Api.calc_history()


