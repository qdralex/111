import sqlite3
from models import *
import datetime
import array

class DbManager:
    def __init__(self, db_path):
        self.db_path = db_path
        try:
            self.con = sqlite3.connect(db_path)
            self.cur = self.con.cursor()
        except Exception as err:
            print('start   %s' % (str(err)) )

        sql_create_res_his_table = """CREATE TABLE IF NOT EXISTS result_history (
                                            id INTEGER PRIMARY KEY,
                                            img TEXT,
                                            predicts TEXT,
                                            date_press TEXT,
                                            time_press TEXT
                                        );"""

#NOT NULL REFERENCES result_history(id)
        sql_create_use_his_table = """CREATE TABLE IF NOT EXISTS usage_history (
                                            id integer,
                                            date TEXT,
                                            time TEXT
                                        );"""

        self.cur.execute(sql_create_res_his_table)
        self.cur.execute(sql_create_use_his_table)

    #   create_table()
        
    def get_all_result_history(self):
        for row in self.cur.execute("SELECT * FROM result_history ORDER BY id"):
            print(row)
            
    def insert_history(self, id, date, time):
        self.cur.execute(f"INSERT INTO usage_history(id, date, time) VALUES (?, ?, ?)", (id, date, time))
        self.con.commit()
        
    def insert_result(self, img, predicts, id, date_press, time_press):
        self.cur.execute(f"INSERT INTO result_history(img, predicts, date_press, time_press, id) VALUES (?, ?, ?, ?, ?)", (img, predicts, date_press, time_press, id))
        self.con.commit()
        
    def get_all_result_with_usage(self):
        rows = self.cur.execute(f"SELECT result_history.img, result_history.predicts, result_history.date_press, result_history.time_press FROM result_history")
        result = []
        for row in rows:
            result.append(Result(row[0], row[1], row[2], row[3]))
        return result
        
    def get_last_inserted_row_id(self):        
        return self.cur.lastrowid

    def close(self):
        self.con.close()
    def get_row_qty(self):
        cursor = self.cur.execute(f"SELECT max(id) FROM result_history")
        sense = cursor.fetchone()[0]
        if sense == None:
            return 0
        else:
            return sense+1



#today = datetime.datetime.today().strftime("%m/%d/%Y")





#db.get_all_result_with_usage()


#for i in range(0, 10):
#    db = DbManager('db.db')
#    print(i)
#    db.insert_result("avasvcasvasvasvasvavasvasvasv", "Залупа", i, "2023-11-22", "19-25")
    #db.insert_history(id, "2023-11-22", "19-25")
#    print(db.get_last_inserted_row_id())
    #db.close()

#print(db.get_all_result_with_usage())

#for j in range(0, 2):
#    db = DbManager('db.db')
#    i = db.get_row_qty()
#    print(i)
    #db.insert_result("avasvcasvasvasvasvavasvasvasv", "Залупа", i, "2023-11-22", "19-25")
    #db.insert_history(id, "2023-11-22", "19-25")
    #print(db.get_last_inserted_row_id())
