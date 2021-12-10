import mysql.connector
from mysql.connector import errorcode
import re
from web.config import mysql_config
from web.config import get_config

def run_mysql(sql,data):
    config = get_config()
    try:
        conn = mysql.connector.connect(
            user=config.DB_USER,
            passwd=config.DB_PASSWORD,
            db=config.DB_NAME
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


def get_result(cur, sql, data):
    cur.execute(sql, data)
    columns = cur.description
    result = [{columns[index][0]: column for index, column in enumerate(value)} for value in cur.fetchall()]
    return result


def query_mysql(sql, data, pagination=False):
    config = get_config()
    try:
        conn = mysql.connector.connect(
            user=config.DB_USER,
            passwd=config.DB_PASSWORD,
            db=config.DB_NAME
        )
        cur = conn.cursor()
        result = get_result(cur, sql, data)
        if pagination:
            cur.execute('SELECT FOUND_ROWS()', '')
            (total_rows,) = cur.fetchone()
            if total_rows > 0 and len(result) == 0:
                sql = re.sub(r'(?<=OFFSET\s)[0-9]+', "0", sql)

                result = get_result(cur, sql, data)
            pattern = re.compile(r'(?<=LIMIT\s)[0-9]+')
            pattern2 = re.compile(r'(?<=OFFSET\s)[0-9]+')
            page_size = pattern.findall(sql)[0]
            page_offset = pattern2.findall(sql)[0]
            current_page = (int(page_offset)/int(page_size)) + 1

            result = {
                'data': result,
                'currentPage': current_page,
                'pageSize': int(page_size),
                'total': total_rows
            }
        cur.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def query_one(sql, data):
    config = get_config()
    try:
        conn = mysql.connector.connect(
            user=config.DB_USER,
            passwd=config.DB_PASSWORD,
            db=config.DB_NAME
        )
        cur = conn.cursor()
        cur.execute(sql, data)
        columns = cur.description
        row = cur.fetchone()
        result = None
        if row:
            result = {description[0]: row[col] for col, description in enumerate(columns)}
        cur.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)