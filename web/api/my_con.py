import mysql.connector
from mysql.connector import errorcode

from web.config import mysql_config

def run_mysql(sql,data):
    try:
        conn = mysql.connector.connect(
            user=mysql_config['user'],
            passwd=mysql_config['pwd'],
            db=mysql_config['dbname']
        )
        cur = conn.cursor()
        cur.execute(sql, data)
        msg = conn.commit()  #这个对于增删改是必须的，否则事务没提交执行不成功
        cur.close()
        conn.close()
        return msg
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

def query_mysql(sql,data):
    try:
        conn = mysql.connector.connect(
            user=mysql_config['user'],
            passwd=mysql_config['pwd'],
            db=mysql_config['dbname']
        )
        cur = conn.cursor()
        cur.execute(sql, data)
        row = cur.fetchall()
        cur.close()
        conn.close()
        return row
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)